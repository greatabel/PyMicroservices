import unittest
import json
from ch02flask_basic import app as tested_app


class TestApp(unittest.TestCase):
    def test_help(self):
        app = tested_app.test_client()

        hello = app.get('/api')

        body = json.loads(str(hello.data, 'utf8'))
        self.assertEqual(body['Hello'], 'World!')

if __name__ == '__main__':
    unittest.main()