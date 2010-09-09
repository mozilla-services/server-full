VIRTUALENV = virtualenv
BIN = bin
HG = hg

.PHONY: all build 

all:	build

# XXX we could switch to zc.buildout here
build:
	$(VIRTUALENV) --no-site-packages .
	cd deps/sync-core
	$(BIN)/python setup.py develop
	cd ../sync-reg
	$(BIN)/python setup.py develop
	cd ../sync-storage
	$(BIN)/python setup.py develop
	cd ../..
	$(BIN)/python setup.py develop
