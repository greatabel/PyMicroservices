import unittest
import json
from ch02flask_basic import app as tested_app


class TestApp(unittest.TestCase):
    def test_help(self):
        app = tested_app.test_client()


if __name__ == '__main__':
    unittest.main()