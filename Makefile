DEPS = server-core,server-reg,server-storage
VIRTUALENV = virtualenv
PYTHON = bin/python
NOSE = bin/nosetests -s --with-xunit
TESTS = deps/server-core/services/tests deps/server-reg/syncreg/tests deps/server-storage/syncstorage/tests
SERVER = dev-auth.services.mozilla.com
SCHEME = https
BUILDAPP = bin/buildapp
BUILDRPMS = bin/buildrpms
PYPI = http://pypi.python.org/simple
PYPIOPTIONS = -i $(PYPI)
CHANNEL = prod
INSTALL = bin/pip install
INSTALLOPTIONS = -U -i $(PYPI)

ifdef PYPIEXTRAS
	PYPIOPTIONS += -e $(PYPIEXTRAS)
	INSTALLOPTIONS += -f $(PYPIEXTRAS)
endif

ifdef PYPISTRICT
	PYPIOPTIONS += -s
	ifdef PYPIEXTRAS
		HOST = `python -c "import urlparse; print urlparse.urlparse('$(PYPI)')[1] + ',' + urlparse.urlparse('$(PYPIEXTRAS)')[1]"`

	else
		HOST = `python -c "import urlparse; print urlparse.urlparse('$(PYPI)')[1]"`
	endif
	INSTALLOPTIONS += --install-option="--allow-hosts=$(HOST)"

endif

INSTALL += $(INSTALLOPTIONS)


.PHONY: all build update test build_rpms


all:	build

build:
	$(VIRTUALENV) --no-site-packages --distribute .
	$(INSTALL) MoPyTools
	$(INSTALL) Nose
	$(INSTALL) WebTest
	$(BUILDAPP) -c $(CHANNEL) $(PYPIOPTIONS) $(DEPS)

update:
	$(BUILDAPP) -c $(CHANNEL) $(PYPIOPTIONS) $(DEPS)

test:
	$(NOSE) $(TESTS)

build_rpms:
	$(BUILDRPMS) -c $(CHANNEL) $(DEPS)
