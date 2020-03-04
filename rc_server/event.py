import shlex
from subprocess import Popen
from subprocess import PIPE

class Event:
    def __init__(self, event, icon_path=None, exec_cmd=None, exec_hotkey=None):

        self.icon_path = icon_path
        self.event = event
        self.exec_cmd = exec_cmd
        self.exec_hotkey = exec_hotkey

    def has_icon_path(self):
        return self.icon_path is not None

    def has_exec_cmd(self):
        return self.exec_cmd is not None

    def has_exec_hotkey(self):
        return self.exec_hotkey is not None

    def run_exec_cmd(self):
        if self.exec_cmd is not None:
            args = shlex.split(self.exec_cmd)
            p = Popen(args, stdout=PIPE, stderr=PIPE)
            return p

    def run_exec_hotkey(self):
        if self.exec_hotkey is not None:
            args = shlex.split(self.exec_hotkey)
            args = ['xdotool', 'key'] + args
            p = Popen(args,stdout=PIPE, stderr=PIPE)
            return p

