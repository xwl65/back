import  requests
import datetime
from tests.base_testcase import BaseTestCase
class TestLogin():
    def test_useradd(self):
        r=requests.post('http://127.0.0.1:5000/registerapi',
                      json={
                          'username': 'xwl123',
                          "password": '12345',
                          'email'   : 'xwl@126.com'
                      }
                      )
        assert  r.status_code ==200
        assert r.json()['msg']  == 'ok'