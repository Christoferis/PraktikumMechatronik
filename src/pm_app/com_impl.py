'''
Actual implementation of the interfaces and classes described in com.py
'''
from com import transport_protocol, communication protocol
from threading import Thread
from analog import mapping


class com_impl(communication_protocol):

    # blocking by writing a value under the right key (boolean?)
    self.waiting = dict()
    self.tp = None

    def __init__(self, ip, port):
        # create a transport Protocol with given values
        self.tp = TransportProtocol(ip, port, self)


    def _acquire(self, command):            

        pass

    pass