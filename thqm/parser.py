from configparser import ConfigParser
from pathlib import Path

from .event import Event

class Parser:
    def __init__(self, config_path):
        self.config_path = Path(config_path)

    def parse(self):
        cf = ConfigParser()
        cf.read(self.config_path)
        events = {}
        auth = {'password': None}
        for section in cf.sections():
            if section == 'thqm-auth':
                auth = cf._sections[section]
            else:
                events[section] = Event(section, **cf._sections[section])
        return events, auth

