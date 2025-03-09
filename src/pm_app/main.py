# setup logging
import logging
from constants import MIN_LOG_LVL
from com import pm_CommunicationProtocol
from gp_layer import instance as gp_instance
from tkinter import Tk
from ui import instance as ui_instance

root = Tk()
root.title("Robot Control")

logging.basicConfig(format='[%(levelname)s] %(message)s', level=MIN_LOG_LVL)

# create com_impl instance
com = pm_CommunicationProtocol("localhost", 23000)

gp_instance(com)
ui_instance(com, root=root)
