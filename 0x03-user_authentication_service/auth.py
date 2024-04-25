#!/usr/bin/env python3
"""Module for authentication"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
    """hashes password using bcript.hashpw"""

    return hashpw(password.encode('utf-8'), gensalt())

def _generate_uuid() -> str:
    """Generates a unique identification number"""
    return str(uuid4())


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
        
    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user"""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
    
    def create_session(self, email: str) -> str:
        """Creates a new session_id"""
        try:
            user = self._db.find_user_by(email=email)
            ses_id = _generate_uuid()
            user.session_id = ses_id
            return ses_id
        except NoResultFound:
            return None
