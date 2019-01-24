from observer import ObserverPlugin
from observer import st
import re


class InputPlugin(ObserverPlugin):
    def __init__(self, outputs, plugin_name):
        ObserverPlugin.__init__(self, 'input', plugin_name)
        self._rules = self.prepare_rules()
        self._outputs = outputs

    def prepare_rules(self):
        rules = []
        print(self._plugin_name, self._options)
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

    def match(self, text):
        st.ST.debugger().print('Match text', text)
        for rule in self._rules:
            if st.ST.debugger().enabled():
                st.ST.debugger().print('Positive match', {'pattern': rule['pattern']['positive'], 'match': rule['pattern']['positive'].match(text)})
                st.ST.debugger().print('Negative match', {'pattern': rule['pattern']['negative'], 'match': self.match_negative(rule, text)})
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

    def send_message_to_router(self, msg, match_result):
        self._outputs.send_message(msg, match_result)
