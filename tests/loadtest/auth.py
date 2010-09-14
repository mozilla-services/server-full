import random
import json
import unittest

import patch

from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import Data


class AuthTest(FunkLoadTestCase):

    def setUp(self):
        self.root = self.conf_get('main', 'url')
        self.vusers = int(self.conf_get('main', 'vusers'))
        self.num_wbos = int(self.conf_get('main', 'num_wbos'))

    def test_auth(self):
        username = 'funkloaduser%d' % random.randint(0, self.vusers-1)
        self.setBasicAuth(username, 'x' * 10)

        # GET /1.0/username/info/collections
        res = self.get(self.root + '/1.0/%s/info/collections' % username)
        self.assertEquals(res.code, 200)


if __name__ == '__main__':
    unittest.main()
