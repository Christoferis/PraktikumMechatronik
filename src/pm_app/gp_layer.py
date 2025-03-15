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
from constants import MAX_AXIS, AXIS_RANGE


com_INSTANCE = None

# input is tuple
def cb_left(xy: tuple[int, int]):
    com_INSTANCE.sendjoystick("l", (int((AXIS_RANGE / MAX_AXIS) * xy[0] + AXIS_RANGE), int((AXIS_RANGE / MAX_AXIS) * xy[1] + AXIS_RANGE)))
    update_left(xy)

def cb_right(xy: tuple[int, int]):
    com_INSTANCE.sendjoystick("r", (int((AXIS_RANGE / MAX_AXIS) * xy[0] + AXIS_RANGE), int((AXIS_RANGE / MAX_AXIS) * xy[1] + AXIS_RANGE)))
    update_right(xy)

# input is single value
def cb_dpad(dpad_state: int):
    com_INSTANCE.senddpad(dpad_state)
    update_dpad(dpad)

# input is list
def cb_buttons(states: list[bool]):
    com_INSTANCE.sendbuttons(states)
    update_buttons(states)

def instance(com):
    global com_INSTANCE
    com_INSTANCE = com

    gph = gamepad.GamepadHandler(freq=100)
    gph.add_left_stick_callback(cb_left, gph.CB_ACTION)
    gph.add_right_stick_callback(cb_right, gph.CB_ACTION)
    gph.add_dpad_callback(cb_dpad, gph.CB_CHANGED)
    gph.add_all_buttons_callback(cb_buttons, gph.CB_CHANGED)
    gph.start()