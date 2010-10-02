# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Sync Server
#
# The Initial Developer of the Original Code is the Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Tarek Ziade (tarek@mozilla.com)
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
"""
Basic web fuzzing tool. will send trash
"""
import socket
import random
import string
import sys
import base64

ALLOWED_CODES = ['404', '401', '200', '400']
HOST = 'localhost'
PORT = 5000
USER = 'test_user_96869'
PASS = 'x' * 9
PATHS = ['/user/1.0/__randomu__', '/user/1.0/__random__/node/weave',
         '/user/1.0/__random__/password_reset',
         '/1.0/__randomu__/info/collections',
         '/1.0/__randomu__/info/collection_usage',
         '/1.0/__randomu__/info/collection_counts',
         '/1.0/__randomu__/info/quota',
         '/1.0/__randomu__/storage/__random__',
         '/1.0/__randomu__/storage/__random__/__random__']

def randheaders(auth=False):
    headers = ['User-Agent: Fuzzer']
    if random.randint(1, 3) == 2 and not auth:
        # return bad auth header
        headers.append('Authorization: Basic %s' % randtext(10))
    elif auth:
        # Create a real valid auth
        token = base64.encodestring('%s:%s' % (USER, PASS))
        headers.append('Authorization: Basic %s' % token)
    if random.randint(1, 3) == 1:
        # return bad auth header
        headers.append('X-If-Unmodified-Since: %s' % randtext(10))
    return '\r\n'.join(headers)

def randtext(size=None):
    if size is None:
        if random.randint(0, 50) == 5:
            size = random.randint(500, 1000)
        else:
            size = random.randint(4, 15)
    return ''.join([random.choice(string.ascii_letters) for i in range(size)])

def _GET(auth):
    path = random.choice(PATHS)
    path = path.replace('__random__', randtext())
    if auth:
        path = path.replace('__randomu__', USER)
    else:
        path = path.replace('__randomu__', randtext())

    return "GET %s HTTP/1.0\r\nHost: %s\r\n%s\r\n\r\n" % \
            (path, randheaders(auth), HOST)

def _POST(auth):
    return _DATA(auth)

def _PUT(auth):
    return _DATA(auth, 'PUT')

def _DELETE(auth):
    return _DATA(auth, 'DELETE')

def _DATA(auth=False, method='POST'):
    path = random.choice(PATHS)
    path = path.replace('__random__', randtext())
    if auth:
        path = path.replace('__randomu__', USER)
    else:
        path = path.replace('__randomu__', randtext())

    data = randtext(random.randint(1, 1000))
    return "POST %s HTTP/1.0\r\nHost: %s\r\n%s\r\n\r\n%s" % \
            (path, HOST, randheaders(auth), data)

def build_request(auth):
    return random.choice([_GET, _POST, _PUT, _DELETE])(auth)

def call(auth=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print str(msg)
        sys.exit(1)

    sock.settimeout(2)
    try:
        sock.connect((HOST, PORT))
    except socket.error, msg:
        print str(msg)
        sys.exit(2)

    sock.send(build_request(auth))
    try:
        data = sock.recv(1024)
        res = ''
        while len(data):
            res += data
            data = sock.recv(1024)
        sock.close()
        res = res.split('\n')
        code = res[0].split(' ')[1]
        if code not in ALLOWED_CODES:
            print 'Server failure: %s' % code
            print '\n'.join(res)
            sys.exit(1)
        sys.stdout.write('.')
    except socket.timeout:
        sys.stdout.write('timeout\n')
    except socket.error, e:
        print str(e)

# anonymous + auth calls
for i in range(5000):
    call(random.randint(1, 3) == 2)
    sys.stdout.flush()

print 'Success'
sys.exit(0)

