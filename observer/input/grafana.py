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
        msg['rule_name'] = self.make_rile_name(msg['ruleName'])
        msg['full_message'] = "[{0}] {1}".format(data['ruleName'], data['message'])
        if not msg['evalMatches']:
            msg.pop('evalMatches', None)
            self.send_message_to_router(msg, self._options['outputs'])
        else:
            self.split_msg_and_send_parts(msg)

    def split_msg_and_send_parts(self, msg):
        eval_matches = msg['evalMatches'].copy()
        msg.pop('evalMatches', None)
        for eval_match in eval_matches:
            eval_msg = msg.copy()
            eval_msg['matched_metric'] = eval_match['metric']
            eval_msg['matched_value'] = eval_match['value']
            for key, value in eval_match['tags']:
                eval_msg['matched_tag_{0}'.format(key)] = value
            self.send_message_to_router(msg, self._options['outputs'])
