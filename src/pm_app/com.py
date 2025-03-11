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

class transport_protocol:

    def __init__(self, ip, protocol):
        self.stop = False
        self.sema = Semaphore()
        self.sink = Thread(None, self._background, "Sink")
        self.ip = ip

        # ui bridging -> use IntVar object for everything instead of ping and seperate intvar object 
        self.ping = IntVar()
        
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
                self.ping.set(0)
                pingprogress = True
                self.send("m\r", True)
                pass
            elif pingprogress:
                self.ping.set(time() - counter)
        pass

    def send(self, msg, ping = False):
        with self.sema:
            byte = msg.encode()
            sent = 0

            while sent < len(byte):
                sent += self.socket.send(byte[sent:])
                pass
        pass

        if not ping:
            info("o: " + msg)
        else:
            debug("o: " + msg)

    # returns intvar object
    def get_ping(self):
        return self.ping

    def reconnect(self, ip):
        warning("Reconnecting to " + ip[0] + ":" + str(ip[1]))

        try:
            self.socket.close()
            self.socket = create_connection(ip, 0.1)

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
        raise NotImplementedError
        pass
    pass

# implementation of docs/pm_CommunicationProtocol.md
class pm_CommunicationProtocol(communication_protocol):

    # blocking by writing a value under the right key (boolean?)

    def __init__(self, ip):
        self.waiting = list()
        self.tp = None

        # create a transport Protocol with given values
        self.tp = transport_protocol(ip, self)

    def _acquire(self, command):

        if "ab" in command:
            self.waiting.remove(command.removeprefix("ab"))
        elif "aj" in command:
            pass
        else:
            warning("o: e504")

        pass

    def msg_bundle(self, joystick, dpad_state, buttons):
        msg = ""
        # bundles all information about the controller and sends it to the bot
        # buttons
        for d in enumerate(buttons):
            if d[1] and com_buttons[d[0]] not in self.waiting:
                msg += "b" + com_buttons[d[0]] + ";"
                self.waiting.append(com_buttons[d[0]])

        # dpad (just a single value)
        if dpad_state != dpad_map.NONE and com_dpad[dpad_state] not in self.waiting:
            msg +=  "b" + dpad_map(dpad_state) + ";"
            self.waiting.append(com_dpad[dpad_state])
        
        # joystick
        msg += "jl" + convert_to(joystick[0]) + ";"
        msg += "jr" + convert_to(joystick[1])

        self.tp.send(msg)
        pass

    def close(self):
        self.tp.close()
    
    def get_ping(self):
        return self.tp.get_ping()

    # TODO: Reconnect
    def reconnect(self):
        pass

    pass


if __name__ == "__main__":
    from tkinter import Tk, Button

    f = Tk()

    basicConfig(format='[%(levelname)s] %(message)s', level=DEBUG)
    tp = transport_protocol(("localhost", 23000), communication_protocol())

    Button(f, text="Reconnect", command=lambda: tp.reconnect(ip=tp.ip)).pack()

    f.mainloop()
