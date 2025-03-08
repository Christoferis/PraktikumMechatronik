'''
ProtocolStackV2 compatible logging library using pythons own Logging library
'''

from enum import Enum
import logging

# globals
GLOBAL_LOG_LEVEL = 1
_log = list()
_listener = {log_level.PING : [], log_level.INFO: [], log_level.SPECIAL: [], log_level.CRITICAL: []}

def add_log(string, level = log_level.INFO):
    _log.append((level, string))
    pass

'''
level: at which level the callback should be triggered (if callback should apply to multiple levels: register the same function with different levels)
function: a callback that accepts a String (for the message)
'''
def add_callback(function, level = log_level.INFO):
    _listener[level].append(function)
    pass
