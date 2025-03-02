'''
ProtocolStackV2 compatible logging library
'''

from enum import Enum


# globals
GLOBAL_LOG_LEVEL = 1
_log = list()


class log_level(Enum):
    PING = 0
    INFO = 1
    SPECIAL = 2
    CRITICAL = 3


def add_log(string, level):
    _log.append((string, level))
    pass

def add_log(string):
    _log.append(string)
    pass