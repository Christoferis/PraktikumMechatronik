'''
Based upon test_gamepad found on
https://git.rz.uni-augsburg.de/imech-h/pm-gamepad_layer

Things added:
    - bot communication code
    - protocol window (retractable)
    - actions performed window (list of pressed buttons)
'''

from analog import gamepad
from analog.mapping import GenericPS1ButtonMap as button_map
from analog.mapping import GenericPS1DpadMap as dpad_map
from analog.mapping import AxisMax
from ui import update_left, update_right, update_dpad, update_buttons
from com_impl import INSTANCE

# list(r, l), with l, r: tuple(x,y)
joystick = list()

# booleans corresponding to index
buttons = list()

# booleans corresponding to index
dpad = list()

def cb_left(xy):
    update_left(xy)
    INSTANCE.msg_bundle()

def cb_right(xy):
    update_right(xy)
    INSTANCE.msg_bundle()

def cb_dpad(dpad):
    update_dpad(dpad)
    INSTANCE.msg_bundle()

def cb_buttons(states):
    update_buttons(states)
    INSTANCE.msg_bundle()


#TODO: Decouple UI from Gamepad, add global Array that oversees ALL changes
gph = gamepad.GamepadHandler(freq=100)
gph.add_left_stick_callback(cb_left, gph.CB_CHANGED)
gph.add_right_stick_callback(cb_right, gph.CB_CHANGED)
gph.add_dpad_callback(cb_dpad, gph.CB_CHANGED)
gph.add_all_buttons_callback(cb_buttons, gph.CB_CHANGED)
gph.start()