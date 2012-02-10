# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Bootstrap file -- will try to make sure _build.py is up-to-date, then run it.
"""
import os
import sys
import urllib2


def _rename(path):
    if not os.path.exists(path):
        return

    root = 0
    newname = path + '.bak.%d' % root
    while os.path.exists(newname):
        root += 1
        newname = path + '.bak.%d' % root
    os.rename(path, newname)


def main():
    # getting the file age
    if os.path.exists('._build.etag'):
        with open('._build.etag') as f:
            current_etag = f.read().strip()
        headers = {'If-None-Match': current_etag}
    else:
        headers = {}
        current_etag = None

    request = urllib2.Request('http://moz.ziade.org/_build.py',
                              headers=headers)

    # checking the last version on our server
    try:
        url = urllib2.urlopen(request, timeout=5)
        etag = url.headers.get('ETag')
    except urllib2.HTTPError, e:
        if e.getcode() != 412:
            raise
        # we're up-to-date (precondition failed)
        etag = current_etag
    except urllib2.URLError:
        # timeout error
        etag = None

    if etag is not None and current_etag != etag:
        # we need to update our version
        _rename('_build.py')
        content = url.read()
        with open('_build.py', 'w') as f:
            f.write(content)

        with open('._build.etag', 'w') as f:
            f.write(etag)

    # we're good, let's import the file and run it
    mod = __import__('_build')
    project_name = sys.argv[1]
    deps = [dep.strip() for dep in sys.argv[2].split(',')]
    mod.main(project_name, deps)


if __name__ == '__main__':
    main()
