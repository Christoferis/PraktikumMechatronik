import threading
import time
from analog import joystickapi
from typing import Type, Callable
from enum import Enum


class Gamepad:
    UD_NONE = 0
    UD_ACTION = 1
    UD_CHANGED = 2
    DEADZONE = 1000

    def __init__(self, gid: int = 0):
        """
        Uses windows joystick API to read gamepad data
        :param gid: ID of the gamepad to read (Use find_gamepad() to find the first available gamepad)
        """
        self.gid = gid
        ret, caps = joystickapi.joyGetDevCaps(self.gid)
        if not ret:
            raise Exception("Failed to read gamepad capabilities")
        ret, start_info = joystickapi.joyGetPosEx(self.gid)
        if not ret:
            raise Exception("Failed to read gamepad state")
        self.offsets_xy = (start_info.dwXpos, start_info.dwYpos)
        self.offsets_ru = (start_info.dwRpos, start_info.dwZpos)
        self.num_buttons = caps.wNumButtons
        self.button_states = [False] * self.num_buttons
        self.axis_xy = (0, 0)
        self.axis_ru = (0, 0)
        self.dpad = 0

    def update(self) -> int:
        """
        Reads gamepad and stores the data once
        :return: Update type: UD_CHANGED if any data has changed, UD_ACTION if any data is not zero, UD_NONE otherwise
        """
        ret, info = joystickapi.joyGetPosEx(self.gid)
        update_type = Gamepad.UD_NONE
        if not ret:
            raise Exception("Failed to read gamepad state")

        # Update buttons
        for i in range(self.num_buttons):
            if self.button_states[i] != bool((1 << i) & info.dwButtons):
                self.button_states[i] = not self.button_states[i]
                update_type = Gamepad.UD_CHANGED

        # Update dpad
        dpad_dir = info.dwPOV // 4500
        if self.dpad != dpad_dir:
            self.dpad = dpad_dir
            update_type = Gamepad.UD_CHANGED

        # Update axis
        max_val = 2 ** 15 - 1
        comp_xy = (_clamp(info.dwXpos - self.offsets_xy[0], max_val), _clamp(info.dwYpos - self.offsets_xy[1], max_val))
        comp_ru = (_clamp(info.dwRpos - self.offsets_ru[0], max_val), _clamp(info.dwZpos - self.offsets_ru[1], max_val))
        if comp_xy != self.axis_xy or comp_ru != self.axis_ru:
            self.axis_xy = comp_xy
            self.axis_ru = comp_ru
            update_type = Gamepad.UD_CHANGED

        # Check if there is any action
        if update_type == Gamepad.UD_NONE:
            if (
                    abs(self.axis_xy[0]) > Gamepad.DEADZONE or
                    abs(self.axis_xy[1]) > Gamepad.DEADZONE or
                    abs(self.axis_ru[0]) > Gamepad.DEADZONE or
                    abs(self.axis_ru[1]) > Gamepad.DEADZONE or
                    any(self.button_states) or self.dpad != 14
            ):
                update_type = Gamepad.UD_ACTION
        return update_type

    def get_buttons(self) -> list[bool]:
        """
        Returns the current state of the buttons as a list of booleans
        :return: Button states
        """
        return self.button_states

    def get_axis_xy(self) -> tuple[int, int]:
        """
        Returns the current state of the left stick as a tuple of two integers
        :return: (x, y) values of the left stick
        """
        return self.axis_xy

    def get_axis_ru(self) -> tuple[int, int]:
        """
        Returns the current state of the right stick as a tuple of two integers
        :return: (r, u) values of the right stick
        """
        return self.axis_ru

    def get_dpad(self) -> int:
        """
        Dpad values range from 0 to 7. 0 means North, 1 means North-East, etc. 14 means no direction is pressed
        :return: Dpad value
        """
        return self.dpad


class GamepadHandler:
    CB_ALWAYS = 0
    CB_ACTION = 1
    CB_CHANGED = 2
    CB_NEVER = 3

    def __init__(self, freq: int = 10):
        """
        This updates the gamepad data at a given frequency and calls the registered callbacks.
        Use start() to start the thread.
        :param freq: Frequency of gamepad updates in Hz (Doesn't account for any time taken by the callbacks)
        """
        gid = find_gamepad()
        self.gamepad = Gamepad(gid)
        self.delay = 1 / freq

        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True

        self._cb_btn_map = [None] * self.gamepad.num_buttons
        self._cb_axis_map = [None] * 2
        self._cb_dpad_map = None
        self._cb_allbtn_map = None
        self._cb_btn_types = [self.CB_NEVER] * self.gamepad.num_buttons
        self._cb_axis_types = [self.CB_NEVER] * 2
        self._cb_dpad_type = self.CB_NEVER
        self._cb_allbtn_type = self.CB_NEVER

        self._last_btn_states = [False] * self.gamepad.num_buttons
        self._last_axis_states = [(0, 0), (0, 0)]
        self._last_dpad_state = 14

    def _run(self):
        while True:
            self.gamepad.update()
            btn_states = self.gamepad.get_buttons()
            axis_states = [self.gamepad.get_axis_xy(), self.gamepad.get_axis_ru()]
            dpad_state = self.gamepad.get_dpad()

            # evaluate individual button callbacks
            for i, (cb, cb_type) in enumerate(zip(self._cb_btn_map, self._cb_btn_types)):
                if not cb:
                    continue
                if cb_type == self.CB_ALWAYS or (
                        cb_type == self.CB_ACTION and btn_states[i]) or (
                        cb_type == self.CB_CHANGED and btn_states[i] != self._last_btn_states[i]):
                    cb(btn_states[i])

            # evaluate axis callbacks
            for i, (cb, cb_type) in enumerate(zip(self._cb_axis_map, self._cb_axis_types)):
                if not cb:
                    continue
                if cb_type == self.CB_ALWAYS or (
                        cb_type == self.CB_ACTION and any(axis_states[i])) or (
                        cb_type == self.CB_CHANGED and axis_states[i] != self._last_axis_states[i]):
                    cb(axis_states[i])

            # evaluate dpad and global button callbacks
            if self._cb_dpad_map:
                if self._cb_dpad_type == self.CB_ALWAYS or (
                        self._cb_dpad_type == self.CB_ACTION and dpad_state != 14) or (
                        self._cb_dpad_type == self.CB_CHANGED and dpad_state != self._last_dpad_state):
                    self._cb_dpad_map(dpad_state)
            if self._cb_allbtn_map:
                if self._cb_allbtn_type == self.CB_ALWAYS or (
                        self._cb_allbtn_type == self.CB_ACTION and any(btn_states)) or (
                        self._cb_allbtn_type == self.CB_CHANGED and btn_states != self._last_btn_states):
                    self._cb_allbtn_map(btn_states)

            self._last_btn_states = [btn for btn in btn_states]
            self._last_axis_states = axis_states
            self._last_dpad_state = dpad_state
            time.sleep(self.delay)

    def start(self):
        """
        Starts the update-loop as a separate thread
        """
        self._thread.start()

    def add_button_callback(self, button: [int, Type[Enum]], callback: Callable[[bool], None],
                            cb_type: int = CB_CHANGED):
        """
        Adds a callback for a specific button
        :param button: Button ID or Enum from mapping.py
        :param callback: Callback function that takes a boolean as argument
        :param cb_type: Type of callback: CB_ALWAYS (always call), CB_ACTION (call only when button is pressed),
                        CB_CHANGED (call only when button state changes), CB_NEVER (never call)
        """
        if issubclass(type(button), Enum):
            button = button.value
        self._cb_btn_map[button] = callback
        self._cb_btn_types[button] = cb_type

    def add_left_stick_callback(self, callback: Callable[[tuple[int, int]], None], cb_type: int = CB_CHANGED):
        """
        Adds a callback for the left stick
        :param callback: Callback function that takes a tuple of two integers as argument
        :param cb_type: Type of callback: CB_ALWAYS (always call), CB_ACTION (call only when stick isn't centered),
                        CB_CHANGED (call only when stick moved), CB_NEVER (never call)
        """
        self._cb_axis_map[0] = callback
        self._cb_axis_types[0] = cb_type

    def add_right_stick_callback(self, callback: Callable[[tuple[int, int]], None], cb_type: int = CB_CHANGED):
        """
        Adds a callback for the right stick
        :param callback: Callback function that takes a tuple of two integers as argument
        :param cb_type: Type of callback: CB_ALWAYS (always call), CB_ACTION (call only when stick isn't centered),
                        CB_CHANGED (call only when stick moved), CB_NEVER (never call)
        """
        self._cb_axis_map[1] = callback
        self._cb_axis_types[1] = cb_type

    def add_dpad_callback(self, callback: Callable[[int], None], cb_type: int = CB_CHANGED):
        """
        Adds a callback for the dpad
        :param callback: Callback function that takes an integer as argument
        :param cb_type: Type of callback: CB_ALWAYS (always call), CB_ACTION (call when at least one button is pressed),
                        CB_CHANGED (call only when dpad direction changed), CB_NEVER (never call)
        """
        self._cb_dpad_map = callback
        self._cb_dpad_type = cb_type

    def add_all_buttons_callback(self, callback: Callable[[list[bool]], None], cb_type: int = CB_CHANGED):
        """
        Adds a global callback for all buttons
        :param callback: Callback function that takes a list of booleans as argument, each representing one button
        :param cb_type: Type of callback: CB_ALWAYS (always call), CB_ACTION (call when at least one button is pressed),
                        CB_CHANGED (call only when at least one button state changes), CB_NEVER (never call)
        """
        self._cb_allbtn_map = callback
        self._cb_allbtn_type = cb_type


def _clamp(val, min_max_val):
    return max(min(val, min_max_val), -min_max_val)


def find_gamepad():
    """
    Finds the first available gamepad
    :return: Gamepad ID or None if no gamepad is found
    """
    num = joystickapi.joyGetNumDevs()
    for gid in range(num):
        ret, caps = joystickapi.joyGetDevCaps(gid)

        if ret:
            if "Microsoft" not in caps.szPname:
                continue
            return gid
    else:
        return None
