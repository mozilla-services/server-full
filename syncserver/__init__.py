# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Application entry point.
"""

from mozsvc.config import get_configurator


def includeme(config):
    # For the temporary token-server, use a URL compatible
    # with the planned token-server scheme.  The other vepauth
    # settings are taken from syncstorage app.
    settings = config.registry.settings
    settings.setdefault("who.plugin.vepauth.token_url", "/1.0/sync/2.0")
    config.include("syncstorage")
    config.include("syncreg")
    config.scan("syncserver.views")


def main(global_config, **settings):
    config = get_configurator(global_config, **settings)
    config.include(includeme)
    return config.make_wsgi_app()
