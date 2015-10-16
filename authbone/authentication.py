from functools import wraps
from flask import g


class Authenticator(object):

    IDENTITY_KEY = 'auth_identity'

    def __init__(self, auth_data_getter=None, authenticate_func=None):
        if auth_data_getter:
            self.auth_data_getter = auth_data_getter
        if authenticate_func:
            self.authenticate = authenticate_func

    def is_authenticated(self):
        return hasattr(g, self.IDENTITY_KEY)

    def get_identity(self):
        return getattr(g, self.IDENTITY_KEY)

    def set_identity(self, identity):
        setattr(g, self.IDENTITY_KEY, identity)

    currIdentity = property(get_identity, set_identity)

    def auth_data_getter(self):
        raise NotImplemented()

    def authenticate(self):
        raise NotImplemented()

    def auth_data_validator(self, auth_data):
        return self.authenticate(auth_data)

    def identity_elaborator(self, identity):
        self.currIdentity = identity

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

    def bad_auth_data_callback(self, authDataDecodingEx):
        raise authDataDecodingEx

    def not_authenticated_callback(self, notAuthenticatedEx):
        raise notAuthenticatedEx


def def_bad_auth_data_callback(authDataDecodingEx):
        raise authDataDecodingEx


def def_not_authenticated_callback(notAuthenticatedEx):
        raise notAuthenticatedEx


class AuthDataDecodingException(Exception):
    pass


class NotAuthenticatedException(Exception):
    pass
