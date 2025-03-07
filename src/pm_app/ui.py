'''
Based upon test_gamepad found on
https://git.rz.uni-augsburg.de/imech-h/pm-gamepad_layer

Things added:
    - bot communication code
    - protocol window (retractable)
    - actions performed window (list of pressed buttons)
'''

import tkinter as tk
from tkinter import ttk
from analog import gamepad
from analog.mapping import GenericPS1ButtonMap as button_map
from analog.mapping import GenericPS1DpadMap as dpad_map
from analog.mapping import AxisMax

root = tk.Tk()
root.title("Gamepad Test")

f_sticks = tk.Frame(root)
f_sticks.pack(side=tk.TOP)
f_buttons = tk.Frame(root)
f_buttons.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

f_stick_left = tk.Frame(f_sticks)
f_stick_left.pack(side=tk.LEFT)
f_stick_right = tk.Frame(f_sticks)
f_stick_right.pack(side=tk.RIGHT)

l_buttons = tk.Label(f_buttons, text="Buttons:")
l_buttons.pack(side=tk.LEFT, expand=True, anchor=tk.W)
l_dpad = tk.Label(f_buttons, text=f"DPad: {dpad_map.NONE.name}")
l_dpad.pack(side=tk.RIGHT)

axis_states = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
p_stick_left_y = ttk.Progressbar(f_stick_left, orient=tk.VERTICAL, length=200, mode='indeterminate',
                                 variable=axis_states[1])
p_stick_left_y.pack(side=tk.LEFT)
p_stick_left_x = ttk.Progressbar(f_stick_left, orient=tk.HORIZONTAL, length=200, mode='indeterminate',
                                 variable=axis_states[0])
p_stick_left_x.pack(side=tk.LEFT)

p_stick_right_y = ttk.Progressbar(f_stick_right, orient=tk.VERTICAL, length=200, mode='indeterminate',
                                  variable=axis_states[3])
p_stick_right_y.pack(side=tk.RIGHT)
p_stick_right_x = ttk.Progressbar(f_stick_right, orient=tk.HORIZONTAL, length=200, mode='indeterminate',
                                  variable=axis_states[2])
p_stick_right_x.pack(side=tk.RIGHT)

p_stick_left_y.step(50)
p_stick_left_x.step(50)
p_stick_right_y.step(50)
p_stick_right_x.step(50)

# Protocol Window, Ping and connect Section



def update_left(xy):
    x_val = (xy[0] * 100) // (AxisMax * 2) + 50
    y_val = (xy[1] * 100) // (AxisMax * 2) + 50
    axis_states[0].set(x_val)
    axis_states[1].set(y_val)


def update_right(xy):
    x_val = (xy[0] * 100) // (AxisMax * 2) + 50
    y_val = (xy[1] * 100) // (AxisMax * 2) + 50
    axis_states[2].set(x_val)
    axis_states[3].set(y_val)

def update_dpad(dpad):
    l_dpad.config(text=f"DPad: {dpad_map(dpad).name}")


def update_buttons(states):
    text = "Buttons: " + ", ".join([str(button_map(i).name) for i, state in enumerate(states) if state])
    l_buttons.config(text=text)

root.mainloop()