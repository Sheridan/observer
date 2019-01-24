from observer import ObserverPlugin
import sys


class OutputPlugin(ObserverPlugin):
    def __init__(self, plugin_name):
        ObserverPlugin.__init__(self, 'output', plugin_name)

    def send_message(self, msg, target_name):
        print("You forgot to implement the send_message method")
        sys.exit()

    def target_exists(self, target_name):
        for target in self._options['targets']:
            if target_name == target['name']:
                return True
        return False

    def targets(self):
        targets = []
        for target in self._options['targets']:
            targets.append(target['name'])
        return targets
