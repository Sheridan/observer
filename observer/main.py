from observer.configuration import ConfigParser
from observer import OutputRouter
from observer.input import InputJournald, InputLogfile, InputGrafana
import time
import sys
from observer import st


class Observer:
    def __init__(self):
        super(Observer, self).__init__()
        options = st.ST.options()
        self._output_router = OutputRouter()
        self._inputs = []
        if 'journald' in options['input']:
            self._inputs.append(InputJournald(self._output_router))
        if 'logfile' in options['input']:
            self._inputs.append(InputLogfile(self._output_router))
        if 'grafana' in options['input']:
            self._inputs.append(InputGrafana(self._output_router))
        if not self._inputs:
            print("You forgot to define any input plugin")
            sys.exit()

    def threaded(self):
        for x in self._inputs:
            x.start()
        while True:
            time.sleep(60)
