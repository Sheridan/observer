from systemd import journal
import select
import time
from observer.threadhelper import ThreadHelper
from observer.input.base import InputPlugin


class InputJournald(InputPlugin, ThreadHelper):
    def __init__(self, outputs):
        ThreadHelper.__init__(self)
        InputPlugin.__init__(self, outputs, 'journald')

    def threaded(self):
        j = journal.Reader()
        while True:
            j.seek_tail()
            j.get_previous()

            p = select.poll()
            p.register(j, j.get_events())

            while p.poll():
                if j.process() != journal.APPEND:
                    continue
                for entry in j:
                    if entry['MESSAGE']:
                        self.on_entry(entry)
            time.sleep(1)

    def on_entry(self, entry):
        idnt = entry['SYSLOG_IDENTIFIER'] if entry['SYSLOG_IDENTIFIER'] is not None else 'Unknown'
        match_text = '{0}: {1}'.format(idnt, entry['MESSAGE'])
        match_result = self.match(match_text)
        if match_result:
            msg = self.make_message(match_result['data'])
            msg['full_message'] = entry['MESSAGE']
            msg['identifier'] = entry['SYSLOG_IDENTIFIER']
            msg['timestamp'] = entry['__REALTIME_TIMESTAMP']
            msg['host'] = entry['_HOSTNAME']
            self.send_message_to_router(msg, match_result['rule']['outputs'])
