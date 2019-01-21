import datetime
import socket
import time
import os
from observer.input.base import InputPlugin
from observer import st


class InputLogfile(InputPlugin):
    def __init__(self, outputs):
        super(InputLogfile, self).__init__(outputs, 'logfile')
        self._data = self.storage().load()
        if 'positions' not in self._data:
            self._data['positions'] = {}

    def gen_position_id(self, rule):
        return '{0}:{1}:{2}'.format(rule['path'],
                                    rule['match']['positive'],
                                    rule['match']['negative'] if 'negative' in rule['match'] else 'none')

    def load_file_position(self, rule):
        if rule['name'] not in self._data['positions']:
            self._data['positions'][rule['name']] = -1
        return self._data['positions'][rule['name']]

    def store_file_position(self, rule, position):
        self._data['positions'][rule['name']] = position

    def update_positions(self):
        self.storage().store(self._data)

    def seek_on_file(self, log_stream, rule):
        position = self.load_file_position(rule)
        if position < 0:
            log_stream.seek(0, 2)
            st.ST.debugger().print('Initializing read from end', rule['path'])
        else:
            statinfo = os.stat(rule['path'])
            if statinfo.st_size < position:
                print("Log file {0} truncated".format(rule['path']))
                log_stream.seek(0, 2)
            else:
                log_stream.seek(position, 0)

    def check_log_streams(self, rule):
        with open(rule['path'], 'r') as log_stream:
            self.seek_on_file(log_stream, rule)
            logs = log_stream.read()
            self.store_file_position(rule, log_stream.tell())
            if logs.strip():
                for line in logs.split('\n'):
                    line = line.strip()
                    if line:
                        self.on_entry(line)

    def on_entry(self, entry):
        match_result = self.match(entry)
        if match_result:
            msg = match_result['data']
            msg['full_message'] = entry
            msg['input_plugin_name'] = self.plugin_name()
            msg['identifier'] = match_result['rule']['identifier'] if 'identifier' in match_result['rule'] else 'unset'
            msg['timestamp'] = datetime.datetime.now()
            msg['host'] = socket.gethostname()
            self.send_message_to_router(msg, match_result)

    def run(self):
        while True:
            for rule in self._options['rules']:
                self.check_log_streams(rule)
            self.update_positions()
            time.sleep(1)
