VIRTUALENV = virtualenv
PYTHON = bin/python
HG = hg

.PHONY: all build 

all:	build

# XXX we could switch to zc.buildout here
build:
	$(VIRTUALENV) --no-site-packages .
	cd sync-core; ../$(PYTHON) setup.py develop
	cd sync-storage; ../$(PYTHON) setup.py develop
	cd sync-reg; ../$(PYTHON) setup.py develop
	$(PYTHON) setup.py develop
