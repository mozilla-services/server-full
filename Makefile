VIRTUALENV = virtualenv
PYTHON = bin/python
EZ = bin/easy_install
NOSE = bin/nosetests -s --with-xunit
FLAKE8 = bin/flake8
COVEROPTS = --cover-html --cover-html-dir=html --with-coverage --cover-package=synccore,syncreg,syncstorage
TESTS = deps/sync-core/synccore/tests/ deps/sync-reg/syncreg/tests deps/sync-storage/syncstorage/tests
PKGS = deps/sync-core/synccore deps/sync-reg/syncreg deps/sync-storage/syncstorage
COVERAGE = bin/coverage

.PHONY: all build mysqltest ldaptest test coverage build_extras redistest qa oldtest hudson-coverage

all:	build

# XXX we could switch to zc.buildout here
build:
	$(VIRTUALENV) --no-site-packages --distribute .
	$(PYTHON) build.py

build_extras:
	$(EZ) nose
	$(EZ) coverage
	$(EZ) redis
	$(EZ) flake8
	$(EZ) python-ldap
	$(EZ) mysql-python

mysqltest:
	WEAVE_TESTFILE=mysql $(NOSE) $(TESTS)

ldapltest:
	WEAVE_TESTFILE=ldap $(NOSE) $(TESTS)

redistest:
	WEAVE_TESTFILE=redisql $(NOSE) $(TESTS)

test:
	$(NOSE) $(TESTS)

coverage:
	rm -rf html
	- WEAVE_TESTFILE=mysql $(NOSE) $(COVEROPTS) $(TESTS)
	- WEAVE_TESTFILE=ldap $(NOSE) $(COVEROPTS) $(TESTS)
	- WEAVE_TESTFILE=redisql $(NOSE) $(COVEROPTS) $(TESTS)
	- $(NOSE) $(COVEROPTS) $(TESTS)

hudson-coverage:
	rm -rf html
	- $(COVERAGE) run $(NOSE) $(COVEROPTS) $(TESTS)
	$(COVERAGE) xml

qa:
	rm -rf deps/sync-reg/syncreg/templates/*.py
	$(FLAKE8) $(PKGS)

oldtest:
	cd tests/functional; ../../bin/python run_server_tests.py
