====================================
Setting up a development environment
====================================

Setting up a development environment for Sync consists of cloning the 
main repository and running a make. Before you do this make sure
you have:

- Python 2.6 (default under Debuntu, python26 under CentOS)
- Python 2.6 headers (python2.6-dev under Debuntu, python26-devel under CentOS)
- python26-profiler under Ubuntu
- Mercurial
- Distribute
- Virtualenv 


Then run::

    $ hg clone http://hg.mozilla.com/services/server-full
    $ cd server-full
    $ make build

Once this is done, you can do a sanity check by running all tests::

    $ make test

