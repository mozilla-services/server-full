===========
Code layout
===========

The Sync project is organized into fours repositories:

- **server-core**: contains the core library that provides
  a config reader, a cef logger the authentication back ends, 
  and a base wsgi app.

- **server-reg**: contains the registration application.
  Uses server-core.

- **server-storage**: contains the storage application.
  Uses server-core.

- **server-full**: provides in the same application registration and 
  storage. Can be used to run a standalone server or as a development
  environment.

All the repositories are located in http://hg.mozilla.com/services

