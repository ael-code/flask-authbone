from flask import request
from authentication import AuthDataDecodingException


def simple_data_getter():
    auth_data = dict()
    try:
        auth_data['username'] = request.args['username']
    except KeyError:
        raise AuthDataDecodingException('bad credentials: missing "username"')

    try:
        auth_data['password'] = request.args['password']
    except KeyError:
        raise AuthDataDecodingException('bad credentials: missing "password"')

    return auth_data


def basic_auth_getter():
    return request.authorization
