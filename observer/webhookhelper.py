from observer import st
from observer.threadhelper import ThreadHelper
from bottle import Bottle, request


class WebhookHelper(ThreadHelper, Bottle):
    def __init__(self, interface, port, path):
        ThreadHelper.__init__(self)
        Bottle.__init__(self)
        self._interface = interface
        self._port = port
        self.route(path, ['POST'], self._webhook)

    def _webhook(self):
        self.webhook(request.body.read())

    def webhook(self, body):
        print("You forgot to implement the hook method")
        st.ST.debugger().print('Incoming body', body)

    def threaded(self):
        Bottle.run(self, host=self._interface, port=self._port)
