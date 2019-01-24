import pprint
from observer import st


class Debugger:
    def __init__(self):
        self._debug = st.ST.options()['debug']
        if self._debug:
            self._pp = pprint.PrettyPrinter()

    def enabled(self):
        return self._debug

    def print(self, title, data=None):
        if self._debug:
            header = '-> {0} <------------------'.format(title)
            print(header)
            self._pp.pprint(data)
            print('-' * len(header))
