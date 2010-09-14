.PHONY: bench test report createdb

build:
	virtualenv --no-site-packages --distribute .
	bin/easy_install funkload

createdb:
	bin/fl-run-test createdb.py

test:
	bin/fl-run-test simple.py

bench:
	bin/fl-run-bench simple.py SimpleTest.test_simple

bench_auth:
	bin/fl-run-bench auth.py AuthTest.test_auth

test_auth:
	bin/fl-run-test auth.py 


report:
	bin/fl-build-report --html -o html simple-bench.xml
