# A file for defining constants, like a config file

from platform import system

# Generic Data
PLATFORM = system()

# Default Connection
IP_DEST = "192.168.4.1"
PORT_DEST = "24"

# Protocol
## Transport
# pinginterval: how frequent the ping message should be sent out (as in how long to wait since the previous ping operation has concluded, in seconds)
PINGINTERVAL = 10



# Bytes
MAX_MSG_LEN = 64
