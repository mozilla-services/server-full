VIRTUALENV = virtualenv
PYTHON = bin/python
EZ = bin/easy_install
NOSE = bin/nosetests -s
COVEROPTS = --cover-html --cover-html-dir=html --with-coverage --cover-package=synccore,syncreg,syncstorage
TESTS = deps/sync-core/synccore/tests/ deps/sync-reg/syncreg/tests deps/sync-storage/syncstorage/tests

.PHONY: all build mysqltest ldaptest test coverage

all:	build

# XXX we could switch to zc.buildout here
build:
	$(VIRTUALENV) --no-site-packages --distribute .
	$(PYTHON) build.py

build_extras:
	$(EZ) nose
	$(EZ) coverage

mysqltest:
	WEAVE_TESTFILE=mysql $(NOSE) $(TESTS)

ldapltest:
	WEAVE_TESTFILE=ldap $(NOSE) $(TESTS)

test:
	$(NOSE) $(TESTS)

coverage:
	rm -rf html
	- WEAVE_TESTFILE=mysql $(NOSE) $(COVEROPTS) $(TESTS)
	- WEAVE_TESTFILE=ldap $(NOSE) $(COVEROPTS) $(TESTS)
	- $(NOSE) $(COVEROPTS) $(TESTS)
