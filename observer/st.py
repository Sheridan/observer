import sys

from observer.debuger import Debugger
from observer.configuration.configparser import ConfigParser
from observer.configuration.netproxy import NetProxy


class st:
    def __init__(self):
        self._options = None
        self._storage = None
        self._proxy = None
        self._debugger = None

    def options(self):
        if not self._options:
            self._options = ConfigParser(sys.argv[1]).load()
        return self._options

    def proxy(self):
        if not self._proxy:
            self._proxy = NetProxy()
        return self._proxy

    def debugger(self):
        if not self._debugger:
            self._debugger = Debugger()
        return self._debugger

ST = st()
