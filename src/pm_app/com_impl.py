'''
Actual implementation of the interfaces and classes described in com.py
'''
from com import transport_protocol, communication protocol
from threading import Thread
from analog import mapping
from constants import IP_DEST, PORT_DEST, com_buttons, com_dpad
from gp_layer import joystick, buttons, dpad
from util import csv_typed

INSTANCE = com_pl(IP_DEST, PORT_DEST)


class com_impl(communication_protocol):

    # blocking by writing a value under the right key (boolean?)
    self.waiting = list()
    self.tp = None

    def __init__(self, ip, port):
        # create a transport Protocol with given values
        self.tp = TransportProtocol(ip, port, self)


    def _acquire(self, command):
        self.waiting[command.removeprefix("a")] = false
        pass

    def msg_bundle(self):
        msg = ""
        # bundles all information about the controller and sends it to the bot
        # buttons
        for d in enumerate(buttons):
            if d[1] and d[1] not in self.waiting:
                msg += "b" + com_buttons[d[0]] + ";"
                self.waiting.append(d[1])

        # dpad
        for d in enumerate(dpad):
            if d[1] and d[1] not in self.waiting:
                msg += "b" + com_dpad[d[0]] + ";"
                self.waiting.append(d[1])
        
        # joystick
        msg += "jl" + convert_to(joystick[0]) + ";"
        msg += "jr" + convert_to(joystick[1])

        self.tp(msg)
        pass
    pass