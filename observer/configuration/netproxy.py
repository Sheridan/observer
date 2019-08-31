from observer import st
import urllib.parse

class NetProxy:
    def __init__(self):
        self._requests_proxies = None

    def requests_proxy(self):
        if not self._requests_proxies:
            self._requests_proxies = {}
            proxy = st.ST.options()['proxy']
            if proxy['enabled']:
                prepared_proxy = ""
                if 'user' in proxy:
                    prepared_proxy = '{0}://{1}:{2}@{3}:{4}'.format(
                                        proxy['type'],
                                        urllib.parse.quote(proxy['user']),
                                        urllib.parse.quote(proxy['pass']),
                                        proxy['host'],
                                        proxy['port'])
                else:
                    prepared_proxy = '{0}://{1}:{2}'.format(
                                        proxy['type'],
                                        proxy['host'],
                                        proxy['port'])
                self._requests_proxies = {
                    'http': prepared_proxy,
                    'https': prepared_proxy,
                }
            st.ST.debugger().print("Proxyes: ", self._requests_proxies)
        return self._requests_proxies
