# -*- coding: utf-8 -*-
import json
import unittest
from qfcommon.base import logger
from qfcommon.base.http_client import RequestsClient
from qfcommon.server.client import HttpClient

log = logger.install('stdout')

class TestPayquick(unittest.TestCase):

    def setUp(self):
        self.url = ''
        self.send = {}
        self.host = '127.0.0.1'
        self.port = 7010
        self.timeout = 20000
        self.server = [{'addr':(self.host, self.port), 'timeout':self.timeout},]
        self.client = HttpClient(self.server, client_class=RequestsClient)
        self.headers = {}
        self.cookies = {'csid': 'b19c0021-9b99-4fd7-b5ee-7bdb83c3f98d'}

    @unittest.skip("skipping")
    def test_register(self):
        self.url = '/fenqi/v1/api/user/bind'
        self.send = {
            'mobile': '13802438721',
            'verify_code': '111111',
            'redirect_url': 'http://www.baidu.com'
        }
        ret = self.client.post_json(self.url, self.send, cookies=self.cookies)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_send_sms(self):
        self.url = '/fenqi/v1/api/tools/send'
        self.send = {
            'mobile': '15708478799',
        }
        ret = self.client.post_json(self.url, self.send, cookies=self.cookies)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_user_check(self):
        self.url = '/fenqi/v1/api/user/check/info'
        self.send = {
            'mobile': '13802438721',
            'verify_code': '111111',
        }
        ret = self.client.post_json(self.url, self.send, cookies=self.cookies)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    #@unittest.skip("skipping")
    def test_user_check(self):
        self.url = '/fenqi/v1/api/user/info'
        self.send = {
            'mobile': '13802438721',
            'verify_code': '111111',
        }
        ret = self.client.get(self.url, self.send, cookies=self.cookies)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


suite = unittest.TestLoader().loadTestsFromTestCase(TestPayquick)
unittest.TextTestRunner(verbosity=2).run(suite)
