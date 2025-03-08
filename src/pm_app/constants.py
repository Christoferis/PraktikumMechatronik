# A file for defining constants, like a config file

from platform import system
from logging import DEBUG, WARNING, INFO, CRITICAL

# Generic Data
PLATFORM = system()

# Default Connection
IP_DEST = "192.168.4.1"
PORT_DEST = "24"

# Protocol
## Transport
# pinginterval: how frequent the ping message should be sent out (as in how long to wait since the previous ping operation has concluded, in seconds)
PINGINTERVAL = 5

# Logging
MIN_LOG_LVL = DEBUG

# Bytes
MAX_MSG_LEN = 64

# mapping
com_buttons = ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11")
com_dpad = ("d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7")
