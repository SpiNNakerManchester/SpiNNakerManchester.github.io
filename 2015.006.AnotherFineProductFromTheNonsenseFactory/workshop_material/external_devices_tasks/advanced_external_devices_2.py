import sys
import struct
import Tkinter as tk
from threading import Condition

from spinnman.connections.connection_listener import ConnectionListener
import traceback
from spinnman.connections.udp_packet_connections.udp_connection \
    import UDPConnection
from spinnman.connections.abstract_classes.abstract_listenable \
    import AbstractListenable

if len(sys.argv) < 2:
    print "{} <port>".format(sys.argv[0])
    sys.exit()

port = int(sys.argv[1])


class ListenableUDPConnection(UDPConnection, AbstractListenable):

    def get_receive_method(self):
        return self.receive


directions = [("FORWARD", 0, -10), ("BACKWARD", 0, 10),
              ("LEFT", -10, 0), ("RIGHT", 10, 0)]

root = tk.Tk()
root.title("SimpleBot")
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

pos_x = 250
pos_y = 250
dot = canvas.create_oval(pos_x - 5, pos_y - 5, pos_x + 5, pos_y + 5, fill="red")


print_condition = Condition()


def receive_callback(packet):
    global pos_x
    global pos_y
    global dot
    global canvas

    try:
        count = struct.unpack_from("B", packet, 0)[0]
        for i in range(count):
            key = struct.unpack_from("<H", packet, 2 + (i * 2))[0] & 0x3
            print_condition.acquire()
            direction = directions[key]
            print direction[0]
            canvas.delete(dot)
            pos_x += direction[1]
            pos_y += direction[2]
            dot = canvas.create_oval(pos_x - 5, pos_y - 5, pos_x + 5, pos_y + 5, fill="red")
            print_condition.release()
    except:
        traceback.print_exc()

connection = ListenableUDPConnection(local_port=port)
listener = ConnectionListener(connection)
listener.add_callback(receive_callback)
listener.start()

tk.mainloop()
