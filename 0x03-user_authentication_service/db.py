#!/usr/bin/env python3
"""DB module
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method that creates a User object

        Args:
            email (str): email of the user
            hashed_password (str): password hashed for security

        Returns:
            A User object
        """
        newUser = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(newUser)
            self._session.commit()
        except Exception as e:
            print(f"Error adding user to database: {e}")
            self._session.rollback()
            raise

        return newUser

    def find_user_by(self, **kwargs) -> User:
        """Returns a user based on keyword"""
        try:
            result = self._session.query(User).filter_by(**kwargs).first()

            if result is None:
                raise NoResultFound()

        except TypeError:
            raise InvalidRequestError()

        return result
