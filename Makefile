VIRTUALENV = virtualenv
PYTHON = bin/python
EZ = bin/easy_install
NOSE = bin/nosetests -s --with-xunit
FLAKE8 = bin/flake8
COVEROPTS = --cover-html --cover-html-dir=html --with-coverage --cover-package=synccore,syncreg,syncstorage
TESTS = deps/sync-core/synccore/tests/ deps/sync-reg/syncreg/tests deps/sync-storage/syncstorage/tests
PKGS = deps/sync-core/synccore deps/sync-reg/syncreg deps/sync-storage/syncstorage
COVERAGE = bin/coverage
PYLINT = bin/pylint

.PHONY: all build mysqltest ldaptest test coverage build_extras redistest qa oldtest hudson-coverage lint

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
	$(EZ) mysql-python
	$(EZ) pylint
	$(EZ) pygments
	$(EZ) python-memcached

mysqltest:
	WEAVE_TESTFILE=mysql $(NOSE) $(TESTS)

ldaptest:
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
	rm -f coverage.xml
	- $(COVERAGE) run --source=syncreg,synccore,syncstorage $(NOSE) $(TESTS); $(COVERAGE) xml

lint:
	rm -f pylint.txt
	- $(PYLINT) -f parseable --rcfile=pylintrc $(PKGS) > pylint.txt

qa:
	rm -f deps/sync-reg/syncreg/templates/*.py
	$(FLAKE8) $(PKGS)

oldtest:
	$(PYTHON) tests/functional/run_server_tests.py
