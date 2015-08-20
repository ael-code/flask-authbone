from functools import wraps
from flask import g


class Authenticator(object):

    def __init__(self, auth_data_getter, authenticate_func):
        self.auth_data_getter = auth_data_getter
        self.authenticate = authenticate_func
        self.bad_auth_data_callback = def_bad_auth_data_callback
        self.not_authenticated_callback = def_not_authenticated_callback

    def auth_data_validator(self, auth_data):
        return self.authenticate(auth_data)

    def identity_elaborator(self, identity):
        g.auth_identity = identity

    def perform_authentication(self):
        auth_data = self.auth_data_getter()
        if auth_data is None:
            raise AuthDataDecodingException()
        identity = self.auth_data_validator(auth_data)
        if identity is None:
            raise NotAuthenticatedException()
        self.identity_elaborator(identity)
        return identity

    def requires_authentication(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                self.perform_authentication()
            except AuthDataDecodingException, e:
                return self.bad_auth_data_callback(e)
            except NotAuthenticatedException, e:
                return self.not_authenticated_callback(e)
            return f(*args, **kwargs)
        return decorated


def def_bad_auth_data_callback(authDataDecodingEx):
        raise authDataDecodingEx


def def_not_authenticated_callback(notAuthenticatedEx):
        raise notAuthenticatedEx


class AuthDataDecodingException(Exception):
    pass


class NotAuthenticatedException(Exception):
    pass
