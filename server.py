from klein import Klein
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource

from twisted.internet import task


class PokeServer(WebSocketServerProtocol):

    def onOpen(self):
        self.timer = task.LoopingCall(self.createMonster)
        self.timer.start(60)

    def createMonster(self):
        self.sendMessage('do:createMonster')

    def onMessage(self, payload, isBinary=False):
        pass

    def onClose(self, *args, **kwargs):
        self.timer.stop()


class Application(object):

    app = Klein()

    def __init__(self, ws_url):
        wsFactory = WebSocketServerFactory(ws_url)
        wsFactory.protocol = PokeServer
        self.wsResource = WebSocketResource(wsFactory)

    @app.route('/')
    def index(self, request):
        return open('index.html', 'rb').read()

    @app.route('/ws')
    def ws(self, request):
        return self.wsResource

if __name__ == '__main__':
    port = 5000
    host = '127.0.0.1'
    ws_url = u'ws://{host}:{port}/ws'.format(**locals())
    app = Application(ws_url)
    app.app.run(host, port)
