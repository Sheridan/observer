from observer import ObserverPlugin
from observer import st
import datetime
import socket
import re


class InputPlugin(ObserverPlugin):
    def __init__(self, outputs, plugin_name):
        ObserverPlugin.__init__(self, 'input', plugin_name)
        self._rules = self.prepare_rules()
        self._outputs = outputs

    def make_message(self, data):
        msg = data
        msg['input_plugin_name'] = self.plugin_name()
        msg['timestamp'] = datetime.datetime.now()
        msg['host'] = socket.gethostname()
        return msg

    def prepare_rules(self):
        rules = []
        if 'rules' not in self._options:
            return None
        for rule in self._options['rules']:
            rule['pattern'] = {
                'positive': re.compile(rule['match']['positive']),
                'negative': re.compile(rule['match']['negative']) if 'negative' in rule['match'] and isinstance(rule['match']['negative'], str) and rule['match']['negative'] != '' else None
            }
            rules.append(rule)
        return rules

    def match_negative(self, rule, text):
        return rule['pattern']['negative'] and rule['pattern']['negative'].search(text)

    def match_rules(self, text):
        st.ST.debugger().print('Match text', text)
        for rule in self._rules:
            match_result = self.match_rule(rule, text)
            if match_result:
                return match_result
        return None

    def match_rule(self, rule, text):
        st.ST.debugger().print('Match text', text)
        if st.ST.debugger().enabled():
            st.ST.debugger().print('Positive match', {
                'pattern': rule['pattern']['positive'], 'match': rule['pattern']['positive'].match(text)})
            st.ST.debugger().print('Negative match', {
                'pattern': rule['pattern']['negative'], 'match': self.match_negative(rule, text)})
        if not self.match_negative(rule, text):
            match_result = rule['pattern']['positive'].match(text)
            if match_result:
                data = match_result.groupdict()
                data['rule_name'] = rule['name']
                return {
                    'rule': rule,
                    'data': data
                }
        return None

    def send_message_to_router(self, msg, output_targets):
        self._outputs.send_message(msg, output_targets)

    def make_rile_name(self, text):
        return re.sub(r'[^0-9a-zA-Z]+', '_', text.lower())
