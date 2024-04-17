#!/usr/bin/env python3
"""Authentication module"""
from flask import request


class Auth:
    """Manages API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required"""
        if path is None or not excluded_paths:
            return True
        for i in excluded_paths:
            if i.endswith('*') and path.startswith(i[:-1]):
                return False
            elif i in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Validates authorisation request header"""
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """An instance of current user"""
        return None
