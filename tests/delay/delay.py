""" Simulates a heavy load
"""
import sys
import time
import random

from twisted.internet import reactor
from twisted.protocols import portforward

CURRENT = 0.
MAX_DELAY = 5.
GROWTH = .1
RANDOM_DELAYS = (2., 5., 7.)
RANDOM_RATIO = 100.


class LoggingProxyServer(portforward.ProxyServer):

    def dataReceived(self, data):
        if random.randint(1, RANDOM_RATIO) == 1:
            delay = random.choice(RANDOM_DELAYS)
        else:
            global CURRENT
            global GROWTH

            if CURRENT > MAX_DELAY:
                GROWTH = -.2
            elif CURRENT <= abs(GROWTH):
                GROWTH = .2
            CURRENT += GROWTH
            delay = CURRENT

        print 'Delaying call for %.1fs' % delay
        time.sleep(delay)
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
