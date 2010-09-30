""" Simulates a heavy load
"""
import sys
import time

from twisted.internet import reactor
from twisted.protocols import portforward

CURRENT = 0.
MAX_DELAY = 2.
GROWTH = .2

class LoggingProxyServer(portforward.ProxyServer):

    def dataReceived(self, data):
        global CURRENT
        global GROWTH

        if CURRENT > MAX_DELAY:
            GROWTH = -.2
        elif CURRENT <= abs(GROWTH):
            GROWTH = .2
        CURRENT += GROWTH
        print 'Delaying call for %.1fs' % CURRENT
        time.sleep(CURRENT)
        portforward.ProxyServer.dataReceived(self, data)


class LoggingProxyFactory(portforward.ProxyFactory):
    protocol = LoggingProxyServer

if __name__ == '__main__':
    port = int(sys.argv[1])
    fwdserver = sys.argv[2]
    fwdport = int(sys.argv[3])
    fwd = LoggingProxyFactory(fwdserver, fwdport)
    print('Forwarding from %s to %s:%s with delays' % \
            (port, fwdserver, fwdport))
    reactor.listenTCP(port, fwd)
    reactor.run()
