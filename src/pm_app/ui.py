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
from constants import MIN_LOG_LVL
from logging import root as logger
import logging

# attributes

l_dpad = None
axis_states = []
l_buttons = None

# classes
class window_log_handler(logging.Handler):

    def __init__(self, window: tk.Text, combo, level = logging.INFO):
        super().__init__()
        self.window = window
        self.level = level
        self.combo = combo

    def emit(self, record):

        if record.levelno >= self.level:
            self.window.config(state="normal")
            self.window.insert("1.0", "[" + record.levelname + "] " + record.msg + "\n")
            self.window.config(state="disabled")

    #clears the entire window
    def clear_window(self):
        self.window.config(state="normal")
        self.window.delete("1.0", "end")
        self.window.config(state="disabled")
    
    # change of level should also clear the window
    def change_level(self, level):
        if self.level != level:
            self.level = level
            self.clear_window()

# functions
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

# setup

def instance(com, root):
    global l_dpad
    global l_buttons
    global axis_states
    global f_buttons

    # creating root window in main

    gamepad = ttk.Labelframe(root, text="Gamepad")
    gamepad.pack(side=tk.TOP)

    f_sticks = tk.Frame(gamepad)
    f_sticks.pack(side=tk.TOP)
    f_buttons = tk.Frame(gamepad)
    f_buttons.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

    axis_states = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
    f_stick_left = tk.Frame(f_sticks)
    f_stick_left.pack(side=tk.LEFT)
    f_stick_right = tk.Frame(f_sticks)
    f_stick_right.pack(side=tk.RIGHT)

    l_buttons = tk.Label(f_buttons, text="Buttons:")
    l_buttons.pack(side=tk.LEFT, expand=True, anchor=tk.W)
    l_dpad = tk.Label(f_buttons, text=f"DPad: {dpad_map.NONE.name}")
    l_dpad.pack(side=tk.RIGHT)

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
    protocol = tk.LabelFrame(root, text="Protocol")
    protocol.pack(side=tk.BOTTOM)

    connect = tk.Frame(protocol)
    connect.pack(side=tk.RIGHT)

    # conncectivity part
    ping = tk.Label(connect, text="Current Ping: ", textvariable=com.get_ping())
    ping.pack(side=tk.TOP)

    # logging part
    log = tk.Frame(protocol)
    log.pack(side=tk.LEFT)

    logwindow = tk.Text(log, wrap="word", state="disabled")
    logwindow.pack(side=tk.BOTTOM)

    combo_values = ["DEBUG", "INFO", "WARNING", "CRITICAL"]
    logcombo = ttk.Combobox(log, values=combo_values, state="readonly")
    logcombo.set("INFO")
    logcombo.pack(side=tk.TOP)

    # create window log handler
    whandler = window_log_handler(window=logwindow, combo=logcombo)

    # lambda: grabs level from dictionary logging._nameToLevel from the current(index of combo_values) selection
    logcombo.bind("<<ComboboxSelected>>", func=lambda s: whandler.change_level(logging._nameToLevel[combo_values[logcombo.current()]]))

    # add to rootlogger
    logger.addHandler(whandler)

    root.mainloop()


# test
if __name__ == "__main__":
    from com import transport_protocol, communication_protocol
    from tkinter import Tk

    window = Tk()
    window.title("Robot Center")

    t = transport_protocol("localhost", 23000, communication_protocol())

    instance(t, window)