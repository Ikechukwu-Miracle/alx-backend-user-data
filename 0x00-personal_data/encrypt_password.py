#!/usr/bin/env python3
"""Module for password encription"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a given password"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Compares a hashed password with unhashed one"""
    unhashed = bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    return unhashed
