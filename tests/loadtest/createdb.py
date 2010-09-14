import random
import json
import unittest
import sys
import datetime

import patch

from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import Data


_COLS = ['bookmarks', 'forms', 'passwords', 'history', 'prefs', 'tabs']


class SimpleTest(FunkLoadTestCase):

    def setUp(self):
        self.root = self.conf_get('main', 'url')
        self.vusers = int(self.conf_get('main', 'vusers'))
        self.num_wbos = int(self.conf_get('main', 'num_wbos'))

    def test_create_db(self):
        #self._delete_db()

        print('Creating %d users with %d wbos each' % (self.vusers,
                                                       self.num_wbos))
        # let's create 2k users (captcha needs to be deactivated)
        for i in range(self.vusers-1 -66):
            i += 66
            sys.stdout.write('.')
            sys.stdout.flush()
            name = 'funkloaduser%d' % i
            data = {'password': 'x' * 10,
                    'email': '%s@mozilla.com' % name}
            data = Data('application/json', json.dumps(data))
            try:
                res = self.put(self.root + '/user/1.0/%s' % name, data)
            except AssertionError, e:
                print str(e)

            # each user will have 6000 wbos
            self.setBasicAuth(name, 'x' * 10)
            for id_ in range(self.num_wbos-1):
                col = random.choice(_COLS)
                payload = 'a' * 500
                url = "/1.0/%s/storage/%s" % (name, col)
                data = [{'id': id_, 'payload': 'a' * 500}]
                data = Data('application/json', json.dumps(data))
                res = self.post(self.root + url, data)
                self.assertEquals(res.code, 200)

            self.clearBasicAuth()

    def _delete_db(self):
        print('Removing old users.')
        for i in range(self.vusers-1):
            name = 'funkloaduser%d' % i
            self.setBasicAuth(name, 'x' * 10)
            for col in _COLS:
                url = '/1.0/user/1.0/%s/%s' % (name, col)
                try:
                    self.delete(self.root + url)
                except AssertionError:
                    pass
            try:
                self.delete(self.root + '/user/1.0/%s' % name)
            except AssertionError:
                pass


if __name__ == '__main__':
    unittest.main()
