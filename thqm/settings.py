import os
import platform
from pathlib import Path

HOME = os.getenv('HOME', os.getenv('USERPROFILE'))
XDG_CONF_DIR = os.getenv('XDG_CONFIG_HOME', Path(HOME) / '.config')

CONF_DIR = Path(XDG_CONF_DIR) / 'thqm'
CONF_FILE = CONF_DIR / 'config'
# MODULE_DIR = Path(__file__).parent

CONF_FILE_DEFAULT = '''\
# This is the configuration file for thqm.
# Here is where you can configure the hotkeys or commands to provide on the
# thqm server.

# Here are some examples:

# If this block is present authentication will be required.
# [thqm-auth]
# password=thqm

# [Raise volume]
# exec_cmd=pactl set-sink-volume @DEFAULT_SINK@ +10%

# [Lower volume]
# exec_cmd=pactl set-sink-volume @DEFAULT_SINK@ -10%

# [Toggle mute]
# exec_cmd=pactl set-sink-mute @DEFAULT_SINK@ toggle

# [Media previous]
# exec_hotkey=XF86AudioPrev

# [Media next]
# exec_hotkey=XF86AudioNext

# [Media play]
# exec_hotkey=XF86AudioPlay

# [Media pause]
# exec_hotkey=XF86AudioPause

# [play/pause]
# exec_hotkey=space

# [scrub back]
# exec_hotkey=Left

# [scrub forward]
# exec_hotkey=Right
'''

PLATFORM = platform.uname()[0]

