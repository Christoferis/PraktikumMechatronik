import socket
import time
import gamepad
import argparse

parser = argparse.ArgumentParser(description='Gamepad server')
parser.add_argument('port', type=int, help='port to listen on')
parser.add_argument('-t', '--type', default='change', choices=['change', 'action', 'always'], help='update type')
parser.add_argument('-f', '--freq', type=int, default=100, help='frequency of gamepad updates')
parser.add_argument('-b', '--blocking', action='store_true', help='wait for ack before sending next update')
args = parser.parse_args()

gamepad_id = gamepad.find_gamepad()
gp = gamepad.Gamepad(gid=gamepad_id)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', args.port))
print("Started server on port", args.port)
server.listen(1)
conn, addr = server.accept()

delay = 1 / args.freq
up_type = {'change': gp.UD_CHANGED, 'action': gp.UD_ACTION, 'always': gp.UD_NONE}[args.type]
while 1:
    update = gp.update()
    buttons = gp.get_buttons()
    axis_xy = gp.get_axis_xy()
    axis_ru = gp.get_axis_ru()
    dpad = gp.get_dpad()

    if (up_type == gp.UD_NONE or
            (up_type == gp.UD_CHANGED and update == gp.UD_CHANGED) or
            (up_type == gp.UD_ACTION and update == gp.UD_ACTION)):
        """
        Axis x  Axis y  Axis r  Axis u  Dpad   Buttons
        [0-1]   [2-3]    [4-5]   [6-7]   [8]    [9-10]
        """
        data = bytearray(11)
        data[0:2] = axis_xy[0].to_bytes(2, signed=True)
        data[2:4] = axis_xy[1].to_bytes(2, signed=True)
        data[4:6] = axis_ru[0].to_bytes(2, signed=True)
        data[6:8] = axis_ru[1].to_bytes(2, signed=True)
        data[8] = dpad
        data[9:11] = sum(1 << i for i, state in enumerate(buttons) if state).to_bytes(2, signed=False)
        conn.sendall(data)
        if args.blocking:
            conn.recv(1)
    time.sleep(delay)
