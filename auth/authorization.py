from flask import g
from functools import wraps

class Authorizator(object):

    def __init__(self, authorization_backend):
        self.authorization_backend = authorization_backend

    def identity_getter(self):
        return g.auth_identity

    def check_capability(self, identity, capability):
        return self.authorization_backend.check_capability(identity, capability)

    def perform_authorization(self, capability):
        if not self.check_capability(self.identity_getter(), capability):
            raise CapabilityMissingException(capability)
        return True

    def requires_capability(self, capability):
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                self.perform_authorization(capability)
                return f(*args, **kwargs)
            return decorated
        return decorator


class CapabilityMissingException(Exception):

    def __init__(self, capability):
        Exception.__init__(self, capability)
