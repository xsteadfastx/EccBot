import datetime
import os
import sys
import time
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl


def log_it(user, msg):
    today = datetime.date.today().isoformat()
    now = time.strftime('[%H:%M:%S]', time.localtime())
    logfile = 'log/%s.log' % today
    with open(logfile, 'a') as f:
        message = '%s <%s> %s\n' % (now, user, msg)
        f.write(message)


class EccBot(irc.IRCClient):
    nickname = 'sherlock'
    password = sys.argv[1]

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        self.msg(channel, 'Ahoi!')

    def action(self, user, channel, msg):
        log_it(user, msg)

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        log_it(user, msg)

        ''' ping '''
        if msg == 'ping':
            self.msg(channel, '%s: pong' % user)


class EccBotFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = EccBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()


if __name__ == '__main__':
    ''' check if log folder exists else create it '''
    if not os.path.exists('log'):
        os.makedirs('log')

    f = EccBotFactory('#it')

    reactor.connectSSL("ecclesianuernberg.de", 6667, f,
                       ssl.ClientContextFactory())

    reactor.run()
