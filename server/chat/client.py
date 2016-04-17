from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted import wamp       # websocket
from autobahn.wamp import auth
from autobahn.wamp.types import PublishOptions


USER = u'other'
PASSWORD = u'hohoho'


class MyFrontendComponent(wamp.ApplicationSession):

    def onConnect(self):
        print("connected. joining realm {} as user {} ...".format(
            self.config.realm, USER))

        print(dir(self))
        self.join(
            self.config.realm,
            [u"wampcra"],
            USER,
        )

    def onChallenge(self, challenge):
        print("authentication challenge received: {}".format(challenge))
        if challenge.method == u"wampcra":
            if u'salt' in challenge.extra:
                key = auth.derive_key(
                    PASSWORD.encode('utf8'),
                    challenge.extra['salt'].encode('utf8'),
                    challenge.extra.get('iterations', None),
                    challenge.extra.get('keylen', None))
            else:
                key = PASSWORD.encode('utf8')

            signature = auth.compute_wcs(
                key, challenge.extra['challenge'].encode('utf8'))
            return signature.decode('ascii')
        else:
            raise Exception(
                "don't know how to compute challenge for authmethod {}".format(
                    challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        print("ok, session joined!")

        topic = 'ja.lafoglia.room.general'

        try:
            yield self.publish(
                topic,
                dict(message='hogehoge', nick='system'),
                options=PublishOptions(acknowledge=True))
            print("ok, event published to topic {}".format(topic))
        except Exception as e:
            print("publication to topic {} failed: {}".format(topic, e))

        self.leave()

    def onLeave(self, details):
        print("onLeave: {}".format(details))
        self.disconnect()

    def onDisconnect(self):
        reactor.stop()


if __name__ == '__main__':

    from autobahn.twisted.wamp import ApplicationRunner

    runner = ApplicationRunner(
        url="ws://localhost:8080/ws", realm="realm1", extra={'xxx': 'yyyy', })
    runner.extra['xxxx'] = 'hoge'
    runner.run(MyFrontendComponent)
