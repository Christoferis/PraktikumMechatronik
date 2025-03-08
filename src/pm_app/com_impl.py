'''
Actual implementation of the interfaces and classes described in com.py
'''
from com import transport_protocol, communication_protocol
from threading import Thread
from analog.mapping import GenericPS1DpadMap as dpad_map
from constants import IP_DEST, PORT_DEST, com_buttons, com_dpad
from gp_layer import joystick, buttons, dpad
from util import csv_typed


INSTANCE = com_impl(IP_DEST, PORT_DEST)

class com_impl(communication_protocol):

    # blocking by writing a value under the right key (boolean?)
    self.waiting = list()
    self.tp = None

    def __init__(self, ip, port):
        # create a transport Protocol with given values
        self.tp = TransportProtocol(ip, port, self)

    def _acquire(self, command):
        # TODO: Redo this because, the fuck was I thinking?

        self.waiting[command.removeprefix("a")] = False
        pass

    def msg_bundle(self, joystick, dpad, buttons):
        msg = ""
        # bundles all information about the controller and sends it to the bot
        # buttons
        for d in enumerate(buttons):
            if d[1] and com_buttons[d[0]] not in self.waiting:
                msg += "b" + com_buttons[d[0]] + ";"
                self.waiting.append(com_buttons[d[0]])

        # dpad (just a single value)
        if dpad != dpad_map.NONE and com_dpad[dpad] not in self.waiting:
            msg +=  "b" + dpad_map(dpad) + ";"
            self.waiting.append(com_dpad[dpad])
        
        # joystick
        msg += "jl" + convert_to(joystick[0]) + ";"
        msg += "jr" + convert_to(joystick[1])

        self.tp.send(msg)
        pass

    def close(self):
        self.tp.close()

    pass

# replaces INSTANCE with a different INSTANCE
def create_new_instance(ip, port):
    try:
        inst = com_impl(ip, port)
        INSTANCE = inst
    except Exception as e:
        print(e)
        pass


