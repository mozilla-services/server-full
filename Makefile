VIRTUALENV = virtualenv
PYTHON = bin/python

.PHONY: all build 

all:	build

# XXX we could switch to zc.buildout here
build:
	$(VIRTUALENV) --no-site-packages --distribute .
	$(PYTHON) build.py
