from observer.webhookhelper import WebhookHelper
from observer.input.base import InputPlugin
from observer import st
import json

LISTEN_INTERFACE = '0.0.0.0'
LISTEN_PORT = 3214


class InputGrafana(InputPlugin, WebhookHelper):
    def __init__(self, outputs):
        InputPlugin.__init__(self, outputs, 'grafana')
        WebhookHelper.__init__(self,
                               self._options['listen']['interface'],
                               self._options['listen']['port'],
                               '/grafana/')

    def check_options(self):
        if 'listen' not in self._options:
            self._options['listen'] = {
                'interface': LISTEN_INTERFACE,
                'port': LISTEN_PORT
            }
        else:
            if 'interface' not in self._options['listen']:
                self._options['listen']['interface'] = LISTEN_INTERFACE
            if 'port' not in self._options['listen']:
                self._options['listen']['port'] = LISTEN_PORT

    def webhook(self, body):
        data = json.loads(body)
        st.ST.debugger().print('Grafana incoming', data)
        msg = self.make_message(data)
        msg['full_message'] = "[{0}] {1}".format(data['ruleName'], data['message'])
        self.send_message_to_router(msg, self._options['outputs'])
