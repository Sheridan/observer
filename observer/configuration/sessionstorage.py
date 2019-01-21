
from observer import st
import yaml
import os


class SessionStorage:
    def __init__(self, plugin_type, plugin_name):
        self._options = st.ST.options()['session_storage']
        self._plugin_type = plugin_type
        self._plugin_name = plugin_name

    def storage_file_name(self):
        return '{0}/{1}_{2}.yaml'.format(self._options['storage_folder'], self._plugin_type, self._plugin_name)

    def load(self):
        filename = self.storage_file_name()
        if os.path.isfile(filename):
            with open(filename, 'r') as stream:
                return yaml.load(stream)
        return {}

    def store(self, data):
        with open(self.storage_file_name(), 'w') as stream:
            stream.write(yaml.dump(data))
