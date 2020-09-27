import  requests
import datetime
from tests.base_testcase import BaseTestCase
class TestLogin(BaseTestCase):
    def test_add(self):
        r=requests.post('http://127.0.0.1:5000/testcase',
                      headers={'Authorization': f'Bearer {self.token}'},
                      json={
                          'name': f'name{str(datetime.datetime.now())}',
                          "description": 'd',
                          'data' : ''
                      }
                      )
        assert  r.status_code ==200
        assert r.json()['msg']  == 'ok'

    def test_delete(self):
        r=requests.delete('http://127.0.0.1:5000/testcase',
                      headers={'Authorization': f'Bearer {self.token}'},
                      json={
                          'name': 'name2020-09-23 10:31:28.300462',
                          "description": 'd',
                          'data' : ''
                      }
                      )
        assert r.json()['msg'] == 'ok'

    def test_testcase_put(self):
        name = 'name2020-09-23 10:47:43.351586'
        description = 'd'
        update_name = 'name2020-09-23 10:47:43.351586xwl'
        update_description = 'dxwl'
        update_data = '更新后数据'
        res = requests.put('http://127.0.0.1:5000/testcase',
                           json={
                               'name': name,
                               'description': description,
                               'update_name': update_name,
                               'update_description': update_description,
                               'update_data': update_data
                           },
                           headers={'Authorization': f'Bearer {self.token}'})

        print(res.json())
        assert res.status_code == 200
        assert res.json()['msg'] == 'update success'