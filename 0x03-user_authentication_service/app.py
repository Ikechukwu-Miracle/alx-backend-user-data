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
        newUser = AUTH.register_user(email, password)
        if newUser:
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
        response = jsonify({"email": "<user email>", "message": "logged in"})
        response.set_cookie("session_id", ses_id)

        return response


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Ends a session"""
    cookie = request.cookies.get("session_id", None)
    if  cookie is None:
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
