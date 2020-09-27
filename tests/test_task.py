import requests
from tests.base_testcase import BaseTestCase
from time import sleep, time

import requests

from core.app import jenkins
from tests.base_testcase import BaseTestCase
class TestTask(BaseTestCase):
    def test_task_post(self):

        pre=jenkins['testcase'].get_last_build().get_number()
        r = requests.post(
            'http://127.0.0.1:5000/task',
            json ={'testcases':'sub_dir'},
            #作为鉴权使用
            headers={'Authorization': f'Bearer {self.token}'}
        )
        assert r.status_code == 200
        #进行等待，等待Jenkins运行任务完成
        for i in range(5):
            if not jenkins['testcase'].is_queued_or_running():
                break
            else:
                sleep(2)

        last = jenkins['testcase'].get_last_build().get_number()
        print(pre)
        print(last)
        assert last == pre +1