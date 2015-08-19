from flask import Flask, g, abort
from authorization import Authorizator
from authentication import Authenticator
from auth_data_getters import simple_data_getter

class AuthenticationBackend(object):

    def authenticate(self, auth_data):
        if auth_data['username'] == 'admin' and auth_data['password'] == 'admin':
            return auth_data
        if auth_data['username'] == 'user' and auth_data['password'] == 'user':
            return auth_data
        return None

class AuthorizationBackend(object):

    def check_capability(self, identity, capability):
        return identity['username'] == 'admin'

authorizator = Authorizator(AuthorizationBackend())

authenticator = Authenticator(simple_data_getter, AuthenticationBackend())

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
@authenticator.requires_authentication
@authorizator.requires_capability(None)
def auth():
    if g.auth_identity:
        return g.auth_identity['username']
    abort(401)

if __name__ == '__main__':
    app.run()
