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
from constants import MAX_MSG_LEN, PINGINTERVAL, CON_RETRY
from logging import warning, info, debug, critical, basicConfig, DEBUG
from time import time, sleep
from tkinter import IntVar
from analog.mapping import GenericPS1DpadMap as dpad_map, GenericPS1ButtonMap as button_map
from util.csv_typed import convert_to

class transport_protocol:

    def __init__(self, ip, protocol):
        self.stop = False
        self.sema = Semaphore(3)
        self.sink = Thread(None, self._background, "Sink")
        self.ip = ip
        self.socket = None

        # ui bridging -> use IntVar object for everything instead of ping and seperate intvar object 
        self.ping = 0
        
        #open socket
        self.reconnect(ip)
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
                char = self.socket.recv(MAX_MSG_LEN)
                buffer += char

                if char == b'':
                    while True:
                        if self.reconnect(self.ip):
                            break

                        sleep(CON_RETRY)
            except ConnectionResetError:

                while True:
                    if self.reconnect(self.ip):
                        break

                    sleep(CON_RETRY)
                pass

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
                    self._send("p")

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
                self._send("m")
                pass
            elif pingprogress:
                self.ping = time() - counter
        pass

    def _send(self, msg: str):
        with self.sema:
            byte = (msg + "\r").encode()
            sent = 0

            while sent < len(byte):
                sent += self.socket.send(byte[sent:])
                pass
        pass

        if msg.startswith("m") or msg.startswith("p"):
            debug("o: " + msg)
        else:
            info("o: " + msg)

    def sendrequest(self, msg: str):
        self._send("r" + msg)

    # returns intvar object
    def get_ping(self):
        return self.ping

    def reconnect(self, ip):
        warning("Reconnecting to " + ip[0] + ":" + str(ip[1]))

        try:

            if self.socket != None:
                self.socket.close()

            self.socket = create_connection(ip, 1)

        except Exception as e:
            critical(e)
            return False
        else:
            warning("Reconnect Successful")
            return True
            pass 

        pass
    pass

class communication_protocol:

    def _accept(self, command):
        pass
    pass

# implementation of docs/pm_CommunicationProtocol.md
class pm_CommunicationProtocol(communication_protocol):

    # blocking by writing a value under the right key (boolean?)

    def __init__(self, ip):
        super().__init__()
        self.waiting = list()
        self.tp = None

        # create a transport Protocol with given values
        self.tp = transport_protocol(ip, self)

    def _acquire(self, command):

        if "ab" in command:
            self.waiting.remove(int(command.removeprefix("ab")))
        elif "aj" in command:
            pass
        else:
            warning("o: e504")

        pass

    def sendjoystick(self, side, xy):
        self.tp.sendrequest("j" + side + convert_to(xy))
        pass

    def sendbuttons(self, buttons):
        pressed = list() 

        for i in enumerate(buttons):
            if i[1] and button_map(i[0]).value not in self.waiting:                
                pressed.append(i[0])
                self.waiting.append(i[0])
                pass

        if pressed:
            self.tp.sendrequest("b" + convert_to(pressed))
        pass

    def senddpad(self, dpad):
        if dpad + 12 not in self.waiting:
            self.waiting(dpad + 12)

        self.tp.sendrequest("b" + str(dpad + 12))
        pass

    def close(self):
        self.tp.close()
    
    def get_ping(self):
        return self.tp.get_ping()

    pass


if __name__ == "__main__":
    from tkinter import Tk, Button

    f = Tk()

    basicConfig(format='[%(levelname)s] %(message)s', level=DEBUG)
    tp = transport_protocol(("localhost", 23000), communication_protocol())

    Button(f, text="Reconnect", command=lambda: tp.reconnect(ip=tp.ip)).pack()

    f.mainloop()
