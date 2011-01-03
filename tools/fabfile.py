from fabric.api import run, get, sudo, put
from fabric.state import env
from fabric import api
from fabric.context_managers import cd

def check_run(cmd):
    res = run(cmd)
    if res.return_code != 0:
        raise ValueError('Command failed (%s)' % cmd)

def check_sudo(cmd):
    res = sudo(cmd)
    if res.return_code != 0:
        raise ValueError('Command failed (%s)' % cmd)

def build_rpms():
    with cd('/home/tarek/server-full'):
        check_run('rm -rf rpms')
        check_run('hg pull && hg up')
        check_run('make build build_rpms')
        check_run('tar -czvf rpms.tgz rpms')
        get('/home/tarek/server-full/rpms.tgz', 'rpms.tgz')
        check_run('rm -f rpms.tgz')

def _deploy(packages):
    put('rpms.tgz', '/tmp/rpms.tgz')
    with cd('/tmp'):
        check_run('tar -xzvf rpms.tgz')

    with cd('/tmp/rpms'):
        check_sudo('cp -r /etc/sync /etc/sync.saved')
        check_sudo('cp -r /etc/nginx/conf.d /etc/nginx/conf.d.old')
        check_sudo('find . -name "python26-services-*.noarch.rpm" '
             '| xargs rpm -F')
        for package in packages:
            check_sudo('find . -name "python26-%s-*.noarch.rpm" '
                        '| xargs rpm -F' % package)
        check_sudo('mv /etc/sync.saved /etc/sync')
        check_sudo('mv /etc/nginx/conf.d.old /etc/nginx/conf.d')
        check_sudo('killall gunicorn nginx')

    check_run('rm -rf /tmp/rpms')
    check_run('rm -f /tmp/rpms.tgz')

def deploy_reg():
    _deploy(['syncreg'])

def deploy_storage():
    _deploy(['syncstorage'])
