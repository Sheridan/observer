from observer.configuration import SessionStorage
from observer import st


class ObserverPlugin:
    def __init__(self, plugin_type, plugin_name):
        self._plugin_type = plugin_type
        self._plugin_name = plugin_name
        self._options = st.ST.options()[self._plugin_type][self._plugin_name]
        self.check_options()
        self._storage = None

    def plugin_name(self):
        return self._plugin_name

    def storage(self):
        if not self._storage:
            self._storage = SessionStorage(self._plugin_type, self._plugin_name)
        return self._storage

    def check_options(self):
        st.ST.debugger().print('Default, dummy options checker for {0}:{1}'.format(self._plugin_type, self._plugin_name))
