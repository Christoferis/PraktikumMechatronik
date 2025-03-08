'''
implements ProtocolStackV2 by Christoferis (christoferis.github.io)
first proposed in Softwareprojekt für Ingenieure

Consists of:
- Transport Protocol
- Communication Protocol
'''

from threading import Thread, Semaphore
from socket import create_connection
# from constants import IP_DEST, PORT_DEST
from constants import MAX_MSG_LEN, PINGINTERVAL
from logging import warning, info, debug, critical
from time import time

class transport_protocol:

    def __init__(self, ip, port, protocol):
        self.stop = False
        self.sema = Semaphore()
        self.ping = 0
        self.sink = Thread(None, self._background, "Sink")
        
        #open socket
        self.socket = create_connection((ip, port), 0.1)
        self.protocol = protocol
        self.sink.start()
        warning("Dispatched Sink Thread")
        pass

    def close(self):
        self.socket.close()
        self.stop = True

    def _background(self):
        counter = time()
        pingprogress = False
        buffer = b''

        while not self.stop:
            msg = ""

            try:
                buffer = buffer.join([self.socket.recv(MAX_MSG_LEN)])
            except TimeoutError:
                pass

            if b'\r' in buffer:
                tup = buffer.partition(b'\r')
                msg = tup[0].decode()
                buffer = tup[2]

            if not (msg.isspace() or msg == ""):

                if msg.startswith("e"):
                    warning("i: " + msg)

                elif msg.startswith("r"):
                    info("i: " + msg)
                    self.protocol._accept(msg.removeprefix("r"))

                elif msg.startswith("m"):
                    debug("i: " + msg)
                    self.send("p\r")

                elif msg.startswith("p"):
                    debug("i: " + msg)
                    pingprogress = False
                    counter = time()
                
                else:
                    add_log("o: e404")
                
            #ping section
            if (time() - counter >= PINGINTERVAL and not pingprogress):
                counter = time()
                self.ping = 0
                pingprogress = True
                self.send("m\r")
                pass
            elif pingprogress:
                self.ping = time() - counter
        pass

    def send(self, msg):
        with self.sema:
            byte = msg.encode()
            sent = 0

            while sent < len(byte):
                sent += self.socket.send(byte[sent:])
                pass
        pass

        add_log("o: " + msg, log_level.INFO)
    pass

class communication_protocol:

    def _accept(self, command):
        pass
    pass

# run thread after init


if __name__ == "__main__":
    tp = transport_protocol("localhost", 23000, communication_protocol())

