from spinnman.transceiver import create_transceiver_from_hostname
import sys

if len(sys.argv) < 4:
    print "{} <machine_name> <x> <y>".format(sys.argv[0])
    sys.exit()

machine_name = sys.argv[1]
x = int(sys.argv[2])
y = int(sys.argv[3])

transceiver = create_transceiver_from_hostname(
    machine_name, 0, auto_detect_bmp=False)
routing_entries = transceiver.get_multicast_routes(x, y)

print "Key        Mask       Links                Cores"
print "===        ====       =====                ====="
for routing_entry in routing_entries:
    print "0x{:08X} 0x{:08X} {:20s} {}".format(
        routing_entry.key_combo, routing_entry.mask,
        list(routing_entry.link_ids), list(routing_entry.processor_ids))
