from flask import request


def simple_data_getter():
    auth_data = dict()
    auth_data['username'] = request.args.get('username', None)
    auth_data['password'] = request.args.get('password', None)
    return auth_data
