#!/usr/bin/env python3
"""Module for authentication"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """hashes password using bcript.hashpw"""

    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializer"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""

        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            newUser = self._db.add_user(email, hashed_password)
            return newUser
