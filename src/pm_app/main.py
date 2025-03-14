# setup logging
import logging
from constants import MIN_LOG_LVL
from com import pm_CommunicationProtocol
from gp_layer import instance as gp_instance
from tkinter import Tk
from ui import instance as ui_instance
from sys import argv

root = Tk()
root.title("Robot Control")

logging.basicConfig(format='[%(levelname)s] %(message)s', level=MIN_LOG_LVL)

print(argv)

# create com_impl instance
com = pm_CommunicationProtocol((argv[1], int(argv[2])))

ui_instance(com, root=root)
gp_instance(com)

root.mainloop()