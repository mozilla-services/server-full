# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from webob.response import Response
from mako.lookup import TemplateLookup

from services.util import (valid_password, text_response, html_response,
                           extract_username)

from syncstorage.storage import get_storage
from syncreg.util import render_mako

from pyramid.security import Authenticated, Allow

from cornice.service import Service

_TPL_DIR = os.path.join(os.path.dirname(__file__), 'templates')
_lookup = TemplateLookup(directories=[_TPL_DIR],
                         module_directory=_TPL_DIR)  # XXX defined in prod


delete_account = Service(name="delete_account", path="/weave-delete-account",
                         acl=lambda r: [(Allow, Authenticated, "authn")],
                         permission="authn")

root = Service(name="root", path="/")

@delete_account.get()
def delete_account_form(request):
    """Returns a form for deleting the account"""
    template = _lookup.get_template('delete_account.mako')
    return html_response(template.render())


@delete_account.post()
def do_delete_account(request):
    """Do the delete."""
    user_name = request.POST.get('username')
    password = request.POST.get('password')
    if user_name is None or password is None:
        return text_response('Missing data')

    auth = request.registry["auth"]
    user_name = extract_username(user_name)
    user_id = auth.authenticate_user(user_name, password)
    if user_id is None:
        return text_response('Bad credentials')

    # data deletion
    get_storage(request).delete_storage(user_id)

    # user deletion (ldap etc.)
    user_id = auth.get_user_id(user_name)
    if user_id is not None:
        res = auth.delete_user(user_id, password)
    else:
        res = True

    if res:
        return text_response('Account removed.')
    else:
        return text_response('Deletion failed.')


@root.get()
def root_is_a_browserid_helper(request):
    from pyramid.response import Response
    return Response("""
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"
        type="text/javascript"></script>
<script src="https://browserid.org/include.js"
        type="text/javascript"></script>
</head>
<body>
<h1>Authentication Required</h1>
<noscript>
This page requires authentication via BrowserID.
Unfortunately your browser does not support JavaScript which is required
for BrowserID login.
</noscript>
<script type="text/javascript">
$(function() {
    // Generate login button in script, so it only appears if
    // we're actually capable of doing it.
    //
    $("<img src='https://browserid.org/i/sign_in_blue.png' id='signin'" +
      "     alt='sign-in button' />").appendTo($("body"));

    // Fire up the BrowserID callback when clicked.
    //
    $("#signin").click(function() {
        navigator.id.getVerifiedEmail(function(assertion) {
            if (assertion) {
                $("<div>").text(assertion).appendTo($("body"));
            }
        });
    });
});
</script>
</body>
    """)
