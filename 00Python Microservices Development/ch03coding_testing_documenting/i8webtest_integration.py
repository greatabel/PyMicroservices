import unittest
import os

# os.environ["HTTP_SERVER"] = "http://localhost:5000"

class TestMyApp(unittest.TestCase):

    def setUp(self):
        # if HTPP_SERVER is set, we use it as an endpoint
        http_app = os.environ.get('HTTP_SERVER')
        print('环境：', http_app)
        if http_app is not None:
            from webtest import TestApp
            self.app = TestApp(http_app)
        else:
            # fallbacks to the wsgi app
            from ch02flask_basic import app
            from flask_webtest import TestApp
            self.app = TestApp(app)
    
    def test_help(self):
        # calling /api/ endpoint
        hello = self.app.get('/api')

        # asserting the body
        self.assertEqual(hello.json['Hello'], 'World!')

if __name__ == '__main__':
    unittest.main()