from observer import st


class NetProxy:
    def __init__(self):
        self._requests = None

    def requests_proxy(self):
        if not self._requests:
            self._requests = {}
            proxy = st.ST.options()['proxy']
            if proxy['enabled']:
                if 'user' in proxy:
                    self._proxies = {
                        proxy['type']: 'socks5://{0}:{1}@{2}:{3}'.format(
                            proxy['user'],
                            proxy['pass'],
                            proxy['host'],
                            proxy['port'])
                    }
                else:
                    self._proxies = {
                        proxy['type']: 'socks5://{0}:{1}'.format(
                            proxy['host'],
                            proxy['port'])
                    }
        return self._requests
