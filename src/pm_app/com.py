'''
implements ProtocolStackV2 by Christoferis (christoferis.github.io)
first proposed in Softwareprojekt für Ingenieure

Consists of:
- Transport Protocol
- Communication Protocol
'''

from threading import Thread
from socket import create_connection
# from constants import IP_DEST, PORT_DEST
from constants import MAX_MSG_LEN, PINGINTERVAL
from log import add_log, log_level
from time import time

class transport_protocol:

    self.thread = None
    self.stop = False
    self.socket = None
    self.connection = None
    self.protocol = None
    self.ping = 0

    def __init__(self, ip, port, protocol):
        #open socket
        self.socket = create_connection((ip, port), 0.1)
        self.protocol = protocol
        self.sink = Thread(None, _background, "Sink", [self])
        self.sink.isDaemon(True)
        self.sink.start()

        print("Dispatched Sink Thread")
        pass

    def close(self):
        self.socket.close()
        self.stop = True


    def _background(self):
        counter = time()
        pingprogress = False

        #TODO: move from blocking to non blocking with try except (or select) https://docs.python.org/3/library/socket.html#notes-on-socket-timeouts

        while not self.stop:
            msg = b''

            try:
                # TODO: Check if stuff received is chunks, stop at \r if so
                msg = self.socket.recv(MAX_MSG_LEN)
            except TimeoutError:
                pass

            if not (msg.isspace() or msg is b''):

                if msg.startswith(b'r'):
                    self.protocol._accept(msg.removeprefix(b'r'))

                elif msg.startswith(b'm'):
                    self.send(b'p\r')

                elif msg.startswith(b'p'):
                    pingprogress = False
                    counter = time()           
                    
                elif msg.startswith(b'e'):
                    add_log(msg.removeprefix(b'e'), log_level.SPECIAL)
                pass

        #ping section

        if (time() - counter >= PINGINTERVAL and not pingprogress):
            counter = time()
            self.ping = 0
            pingprogress = True
            pass
        elif pingprogress:
            self.ping = time() - counter
            



        pass

    def send(self, msg):
        pass

    pass

class communication_protocol:

    def _accept(self, command):
        pass

    pass

# run thread after init
