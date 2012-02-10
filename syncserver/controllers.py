# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""
User controller. Implements all APIs from:

https://wiki.mozilla.org/Labs/Weave/User/1.0/API

"""
import os

from webob.response import Response
from mako.lookup import TemplateLookup

from services.util import (valid_password, text_response, html_response,
                           extract_username)

from syncreg.util import render_mako

_TPL_DIR = os.path.join(os.path.dirname(__file__), 'templates')
_lookup = TemplateLookup(directories=[_TPL_DIR],
                         module_directory=_TPL_DIR)  # XXX defined in prod


class MainController(object):

    def __init__(self, app):
        self.app = app
        self.auth = app.auth.backend

    def delete_account_form(self, request, **kw):
        """Returns a form for deleting the account"""
        template = _lookup.get_template('delete_account.mako')
        return html_response(template.render())

    def do_delete_account(self, request):
        """Do the delete."""
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        if user_name is None or password is None:
            return text_response('Missing data')

        user_name = extract_username(user_name)
        user_id = self.auth.authenticate_user(user_name, password)
        if user_id is None:
            return text_response('Bad credentials')

        # data deletion
        self.app.get_storage(request).delete_user(user_id)

        # user deletion (ldap etc.)
        user_id = self.auth.get_user_id(user_name)
        if user_id is not None:
            res = self.auth.delete_user(user_id, password)
        else:
            res = True

        if res:
            return text_response('Account removed.')
        else:
            return text_response('Deletion failed.')
