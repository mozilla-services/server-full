import random
import sys
import time

from twisted.internet import reactor
from twisted.protocols import portforward

MAX_DELAY =  15


class LoggingProxyServer(portforward.ProxyServer):

    def dataReceived(self, data):
        delay = random.randint(0, MAX_DELAY)
        print 'Delaying call for %d seconds' % delay
        time.sleep(delay)
        portforward.ProxyServer.dataReceived(self, data)


class LoggingProxyFactory(portforward.ProxyFactory):
    protocol = LoggingProxyServer

if __name__ == '__main__':
    port = int(sys.argv[1])
    fwdserver = sys.argv[2]
    fwdport = int(sys.argv[3])
    fwd = LoggingProxyFactory(fwdserver, fwdport)
    print('Forwarding from %s to %s:%s with random delays' % \
            (port, fwdserver, fwdport))
    reactor.listenTCP(port, fwd)
    reactor.run()
