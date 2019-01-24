import requests
from observer.output.base import OutputPlugin
from observer import st


class OutputTelegram(OutputPlugin):
    def __init__(self):
        OutputPlugin.__init__(self, 'telegram')

    def _query(self, method, params=None):
        url = 'https://api.telegram.org/bot{0}/{1}'.format(self._options['token'], method)
        try:
            st.ST.debugger().print('Sending', params)
            r = requests.post(url, data=params, proxies=st.ST.proxy().requests_proxy())
            if r.status_code == 200:
                st.ST.debugger().print('Api return:', r.json())
            else:
                print('API returned status {0}: {1}'.format(r.status_code, r.content()))
        except Exception as e:
            print('Exception {0}'.format(e))

    def send_message(self, msg, target_name):
        for target in self._options['targets']:
            if target['name'] == target_name:
                for room in target['destination']['rooms']:
                    self._query('sendMessage', {
                                'chat_id': room,
                                'text': msg,
                                'disable_web_page_preview': True,
                                'parse_mode': 'HTML'})
                return
