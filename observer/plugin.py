from observer.threadhelper import ThreadHelper
from observer.configuration import SessionStorage
from observer import st


class ObserverPlugin(ThreadHelper):
    def __init__(self, plugin_type, plugin_name):
        self._plugin_type = plugin_type
        self._plugin_name = plugin_name
        self._options = st.ST.options()[self._plugin_type][self._plugin_name]
        self._storage = None

    def plugin_name(self):
        return self._plugin_name

    def storage(self):
        if not self._storage:
            self._storage = SessionStorage(self._plugin_type, self._plugin_name)
        return self._storage
