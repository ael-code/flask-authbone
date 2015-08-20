from flask import Flask, g, Response, abort
from authbone import Authenticator
from authbone.auth_data_getters import basic_auth_getter


def authenticate(auth_data):
    if auth_data.username == 'admin' and auth_data.password == 'admin':
        return {'username': auth_data.username, 'password': auth_data.password}
    return None


def send_401(ex):
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

authenticator = Authenticator(basic_auth_getter, authenticate)
authenticator.bad_auth_data_callback = send_401
authenticator.not_authenticated_callback = send_401

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
@authenticator.requires_authentication
def auth():
    if g.auth_identity:
        return g.auth_identity['username']
    abort(401)

if __name__ == '__main__':
    app.run()
