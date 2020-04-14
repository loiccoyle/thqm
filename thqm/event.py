import shlex
from subprocess import Popen
from subprocess import PIPE

from .settings import PLATFORM

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
            if PLATFORM == "Linux":
                args = self._run_exec_hotkey_linux()
            elif PLATFORM == "Darwin":
                args = self._run_exec_hotkey_darwin()
            else:
                raise OSError(f"I don't know how to execute keypresses on {PLATFORM}.")
            p = Popen(args,stdout=PIPE, stderr=PIPE)
            return p

    def _run_exec_hotkey_darwin(self):
        command = f"echo 'tell application \"System Events\" to keystroke \"{self.exec_hotkey}\"' | osascript"
        return shelx.split(command)

    def _run_exec_hotkey_linux(self):
        args = shlex.split(self.exec_hotkey)
        return ['xdotool', 'key'] + args






