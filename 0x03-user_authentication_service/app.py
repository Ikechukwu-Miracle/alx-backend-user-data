#!/usr/bin/env python3
"""Application Module"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
