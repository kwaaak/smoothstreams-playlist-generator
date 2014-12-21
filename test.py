__author__ = 'Tim'

import unittest
from generate import get_service_url, get_service_port, get_stream_url

class MyTestCase(unittest.TestCase):
    def test_get_service_url(self):
        result = get_service_url('live247')
        desired_result = 'http://smoothstreams.tv/login.php'

        self.assertEqual(desired_result, result)

    def test_get_service_port(self):
        result = get_service_port('rtmp', 'live247')
        desired_result = '2935'

        self.assertEqual(desired_result, result)

if __name__ == '__main__':
    unittest.main()
