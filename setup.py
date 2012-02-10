# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from setuptools import setup

install_requires = ['SyncStorage', 'SyncReg', 'PasteScript']

entry_points = """
[paste.app_factory]
main = syncserver:main

[paste.app_install]
main = paste.script.appinstall:Installer
"""

setup(name='SyncServer',
      version="1.0",
      packages=["syncserver"],
      install_requires=install_requires,
      entry_points=entry_points,
      license='MPLv2.0',
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        ],
)
