# A file for defining constants, like a config file

from platform import system
from logging import DEBUG, WARNING, INFO, CRITICAL
from analog.mapping import GenericPS1DpadMap as dpad

# Generic Data
PLATFORM = system()

# Default Connection
IP_DEST = "192.168.4.1"
PORT_DEST = "24"

# Protocol
## Transport
# pinginterval: how frequent the ping message should be sent out (as in how long to wait since the previous ping operation has concluded, in seconds)
PINGINTERVAL = 0
CON_RETRY = 2

# Logging
MIN_LOG_LVL = DEBUG

# Bytes
MAX_MSG_LEN = 64

# Gamepad
MAX_AXIS = 32767
AXIS_RANGE = 128
