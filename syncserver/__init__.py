# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Application entry point.
"""
from services.baseapp import set_app
from services.wsgiauth import Authentication
from syncserver.controllers import MainController

# XXX alternatively we should use Paste composite feature here
from syncreg.wsgiapp import urls as reg_urls, controllers as reg_controllers
from syncstorage.wsgiapp import (StorageServerApp,
                                 controllers as storage_controllers,
                                 urls as storage_urls)


urls = [('GET', '/weave-delete-account', 'main', 'delete_account_form'),
        ('POST', '/weave-delete-account', 'main', 'do_delete_account')]

urls = urls + reg_urls + storage_urls
reg_controllers.update(storage_controllers)
reg_controllers['main'] = MainController

make_app = set_app(urls, reg_controllers, klass=StorageServerApp,
                   auth_class=Authentication)
