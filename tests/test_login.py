import requests

from tests.base_testcase import BaseTestCase
class TestLogin(BaseTestCase):
    def test_login(self):
        username='xwl65'
        password='123456'
        r=requests.post(
            'http://127.0.0.1:5000/login',

            json={
                'username': username,
                'password': password
            }

        )
        print(r.json())
        assert r.status_code == 200



