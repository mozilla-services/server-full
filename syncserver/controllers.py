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
# The Initial Developer of the Original Code is Mozilla Foundation.
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
User controller. Implements all APIs from:

https://wiki.mozilla.org/Labs/Weave/User/1.0/API

"""
import os

from webob.response import Response
from mako.lookup import TemplateLookup

from services.util import valid_password, text_response, html_response
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
