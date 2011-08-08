APPNAME = server-full
DEPS = server-core,server-reg,server-storage
VIRTUALENV = virtualenv
PYTHON = bin/python
EZ = bin/easy_install
NOSE = bin/nosetests -s --with-xunit
FLAKE8 = bin/flake8
COVEROPTS = --cover-html --cover-html-dir=html --with-coverage --cover-package=syncreg,syncstorage,services
TESTS = deps/server-core/services/tests deps/server-reg/syncreg/tests deps/server-storage/syncstorage/tests
PKGS = deps/server-core/services deps/server-reg/syncreg deps/server-storage/syncstorage
COVERAGE = bin/coverage
PYLINT = bin/pylint
PYPI2RPM = bin/pypi2rpm.py
SERVER = dev-auth.services.mozilla.com
SCHEME = https

.PHONY: all build mysqltest ldaptest test coverage build_extras qa oldtest hudson-coverage lint memcachedtest memcachedldaptest build_rpm2 build_ldap

all:	build

# XXX we could switch to zc.buildout here
build:
	$(VIRTUALENV) --no-site-packages --distribute .
	$(PYTHON) build.py $(APPNAME) $(DEPS)
	$(EZ) -U nose
	$(EZ) -U coverage
	$(EZ) -U flake8
	$(EZ) -U pylint
	$(EZ) -U pygments
	$(EZ) -U python-memcached
	$(EZ) -U pypi2rpm
	$(EZ) WebOb==1.0.7
	$(EZ) -U WebTest
	$(EZ) -U PasteDeploy
	#$(EZ) -U mysql-python
	#$(EZ) -U wsgiproxy
	#$(EZ) -U wsgi_intercept
	#$(EZ) http://ziade.org/python-ldap-2.3.12.tar.gz

memcachedtest:
	WEAVE_TESTFILE=memcached $(NOSE) $(TESTS)

memcachedldaptest:
	WEAVE_TESTFILE=memcachedldap $(NOSE) $(TESTS)

mysqltest:
	WEAVE_TESTFILE=mysql $(NOSE) $(TESTS)

ldaptest:
	WEAVE_TESTFILE=ldap $(NOSE) $(TESTS)

test:
	$(NOSE) $(TESTS)

coverage:
	rm -rf html
	- WEAVE_TESTFILE=mysql $(NOSE) $(COVEROPTS) $(TESTS)
	- WEAVE_TESTFILE=ldap $(NOSE) $(COVEROPTS) $(TESTS)
	- $(NOSE) $(COVEROPTS) $(TESTS)

hudson-coverage:
	cd deps/server-core; hg pull; hg up -C
	cd deps/server-reg; hg pull; hg up -C
	cd deps/server-storage; hg pull; hg up -C
	rm -f coverage.xml
	- $(COVERAGE) run --source=syncreg,syncstorage,services $(NOSE) $(TESTS); $(COVERAGE) xml

lint:
	rm -f pylint.txt
	- $(PYLINT) -f parseable --rcfile=pylintrc $(PKGS) > pylint.txt

qa:
	rm -f deps/server-reg/syncreg/templates/*.py
	$(FLAKE8) $(PKGS)

oldtest:
	$(PYTHON) tests/functional/run_server_tests.py --scheme=$(SCHEME) --server=$(SERVER) --username=$(WEAVE_USER) --password=$(WEAVE_PASSWORD) --secret=$(SECRET)

build_ldap:
	mkdir $(CURDIR)/rpms -p
	wget http://ziade.org/python-ldap-2.3.12.tar.gz
	tar -xzvf python-ldap-2.3.12.tar.gz
	cd python-ldap-2.3.12; ../$(PYTHON) setup.py --command-packages=pypi2rpm.command bdist_rpm2 --dist-dir=$(CURDIR)/rpms --python=python26 --name=python26-ldap
	rm python-ldap-2.3.12.tar.gz
	rm -rf python-ldap-2.3.12

build_rpms:
	rm -rf $(CURDIR)/rpms
	mkdir $(CURDIR)/rpms
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms cef --version=0.2
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms WebOb --version=1.0.7
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms Paste --version=1.7.5.1
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms PasteDeploy --version=1.3.4
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms PasteScript --version=1.7.3
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms SQLAlchemy --version=0.6.6
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms Mako --version=0.4.1
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms Routes --version=1.12.3
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms MarkupSafe --version=0.12
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms simplejson --version=2.1.6
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms MySQL-python --version=1.2.3
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms python-memcached --version=1.47
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms recaptcha-client --version=1.0.6
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms WSGIProxy --version=0.2.2
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms pylibmc --version=1.1.1
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms pymysql
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms pymysql_sa --version=1.0
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms gevent --version=0.13.6
	$(PYPI2RPM) --dist-dir=$(CURDIR)/rpms greenlet --version=0.3.1
	cd deps/server-core; rm -rf build; ../../$(PYTHON) setup.py --command-packages=pypi2rpm.command bdist_rpm2 --spec-file=Services.spec --dist-dir=$(CURDIR)/rpms
	cd deps/server-storage; rm -rf build;../../$(PYTHON) setup.py --command-packages=pypi2rpm.command bdist_rpm2 --spec-file=SyncStorage.spec --binary-only --dist-dir=$(CURDIR)/rpms
	cd deps/server-reg; rm -rf build;../../$(PYTHON) setup.py --command-packages=pypi2rpm.command bdist_rpm2 --spec-file=SyncReg.spec --dist-dir=$(CURDIR)/rpms

bench_one:
	cd tests/loadtest; ../../bin/fl-run-test simple SimpleTest.test_simple

bench:
	cd tests/loadtest; ../../bin/fl-run-bench simple SimpleTest.test_simple
