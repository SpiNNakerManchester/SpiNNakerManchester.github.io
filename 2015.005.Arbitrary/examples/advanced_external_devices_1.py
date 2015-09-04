import sys
import time

from spinnman.connections.udp_packet_connections.udp_eieio_connection \
    import UDPEIEIOConnection
from spinnman.messages.eieio.data_messages.eieio_data_message \
    import EIEIODataMessage
from spinnman.messages.eieio.data_messages.eieio_32bit.eieio_32bit_data_message\
    import EIEIO32BitDataMessage

if len(sys.argv) < 4:
    print "{} <machine-name> <port> <base-key>".format(sys.argv[0])
    sys.exit()

connection = UDPEIEIOConnection(
    remote_host=sys.argv[1], remote_port=int(sys.argv[2]))

base_key = int(sys.argv[3])

keys_to_send = [
    [7], [6, 8], [0, 9], [], [0, 5, 9], [], [0, 4, 9], [1, 3], [2], [], [], [],
    range(0, 10), [], [5, 9], [], [5, 9], [], [5, 9], [6, 8], [7], [], [], [],
    [0, 9], [], [0, 9], [], range(0, 10), [], [0, 9], [], [0, 9], [], [], [],
    range(0, 10), [8], [7], [6], [5], [4], [3], [2], [1], range(0, 10), [], [], [],
    range(0, 10), [8], [7], [6], [5], [4], [3], [2], [1], range(0, 10), [], [], [],
    [0], [1], [2, 3], [4], [5, 6], [5, 7, 8], [5, 9], [5, 7, 8], [5, 6], [4], [2, 3], [1], [0], [], [], [],
    range(0, 10), [4, 5], [3, 6], [2, 7], [1, 8], [0, 9], [], [], [],
    range(0, 10), [0, 5, 9], [0, 5, 9], [0, 5, 9], [0, 5, 9], [0, 9], [0, 9], [], [], [],
    range(0, 10), [], [5, 9], [], [4, 5, 9], [3], [2, 5, 9], [1, 6, 8], [0, 7], [], [], []]
time_between_keys = 0.05
time_between_sequences = 0.2

while True:
    for keys in keys_to_send:
        message = EIEIO32BitDataMessage()
        for key in keys:
            message.add_key(base_key + key)
        connection.send_eieio_message(message)
        time.sleep(time_between_keys)
    time.sleep(time_between_sequences)

