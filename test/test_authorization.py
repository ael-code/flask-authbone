import unittest
from flask import Flask
from authbone import Authorizator, Authenticator
from authbone.auth_data_getters import form_data_getter


users = {'admin': 'admin',
         'test': 'test'}


def authenticate(auth_data):
    try:
        if auth_data['password'] == users[auth_data['username']]:
            return auth_data
    except KeyError:
        return None
    return None


def check_capability(identity, capability):
    return identity['username'] == 'admin'


authenticator = Authenticator(form_data_getter, authenticate)
authorizator = Authorizator(check_capability, authenticator)

app = Flask(__name__)
app.config['TESTING'] = True


@app.route('/')
@authorizator.requires_capability(None)
def root():
    return 'ok'


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.tc = app.test_client()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
