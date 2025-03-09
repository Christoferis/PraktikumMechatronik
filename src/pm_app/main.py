# setup logging
import logging
from constants import MIN_LOG_LVL
from com import pm_CommunicationProtocol
from gp_layer import instance as gp_instance
import ui

logging.basicConfig(format='[%(levelname)s] %(message)s', level=MIN_LOG_LVL)

# create com_impl instance
com = pm_CommunicationProtocol("localhost", 23000)

gp_instance(com)
ui.instance(com)

# import and run other things
import ui