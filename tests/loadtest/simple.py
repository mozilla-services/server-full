import random
import json
import unittest

import patch

from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import Data


collections = ['bookmarks', 'forms', 'passwords', 'history', 'prefs', 'tabs']

class SimpleTest(FunkLoadTestCase):

    def setUp(self):
        self.root = self.conf_get('main', 'url')
        self.vusers = int(self.conf_get('main', 'vusers'))
        self.num_wbos = int(self.conf_get('main', 'num_wbos'))

    def test_simple(self):
        username = 'funkloaduser%d' % random.randint(0, self.vusers-1)
        self.setBasicAuth(username, 'x' * 10)

        # GET /1.0/username/info/collections
        res = self.get(self.root + '/1.0/%s/info/collections' % username)
        self.assertEquals(res.code, 200)

        # GET /1.0/username/storage/collection
        for collection in collections:
            if random.randint(1, 4) == 4:
                url = "/1.0/%s/storage/%s?full=1" % (username, collection)
                res = self.get(self.root + url)
                self.assertEquals(res.code, 200)

        # POST /1.0/username/storage/collection
        for collection in collections:
            if random.randint(1, 4) == 4:
                id = random.randint(1, 100)
                payload = 'a' * 500
                url = "/1.0/%s/storage/%s" % (username, collection)
                data = "[{\"id\": %i, \"payload\": \"%s\"}]" % (id, payload)
                data = Data('application/json', data)
                res = self.post(self.root + url, data)
                self.assertEquals(res.code, 200)


if __name__ == '__main__':
    unittest.main()
