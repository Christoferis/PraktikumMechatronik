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

# single value
dpad = dpad_map.NONE

# input is tuple
def cb_left(xy: tuple[int, int]):
    global joystick
    joystick[1] = xy
    update_left(xy)

def cb_right(xy: tuple[int, int]):
    global joystick
    joystick[0] = xy

    update_right(xy)

# input is single value
def cb_dpad(dpad: int):
    global dpad
    dpad = dpad

    update_dpad(dpad)

# input is list
def cb_buttons(states: list[bool]):

    global buttons, joystick, dpad
    buttons = states
    update_buttons(states)

    # run here to save one thread: CB_ALWAYS will always run this function callback
    # change if sending takes to long
    INSTANCE.msg_bundle(joystick, dpad, buttons)


gph = gamepad.GamepadHandler(freq=100)
gph.add_left_stick_callback(cb_left, gph.CB_ALWAYS)
gph.add_right_stick_callback(cb_right, gph.CB_ALWAYS)
gph.add_dpad_callback(cb_dpad, gph.CB_ALWAYS)
gph.add_all_buttons_callback(cb_buttons, gph.CB_ALWAYS)
gph.start()