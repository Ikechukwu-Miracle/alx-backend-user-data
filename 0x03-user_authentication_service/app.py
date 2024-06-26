#!/usr/bin/env python3
"""Application Module"""
from flask import Flask, jsonify, redirect, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> str:
    """JSON message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """POST /users
    Registers new user in request form-data,
    or finds if user is already registered based on email
    Return:
        - JSON payload of the form containing various information
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """Login route

    Return -
        JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")

    validate_user = AUTH.valid_login(email, password)
    if validate_user is False:
        abort(401)
    else:
        ses_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", ses_id)

        return response


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Ends a session"""
    cookie = request.cookies.get("session_id", None)
    if cookie is None:
        abort(403)

    user = AUTH.get_user_from_session_id(cookie)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """Route to the profile"""
    cookie = request.cookies.get("session_id", None)
    if cookie is None:
        abort(403)

    user = AUTH.get_user_from_session_id(cookie)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """POST /reset_password"""
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password():
    """Reset password end point"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
