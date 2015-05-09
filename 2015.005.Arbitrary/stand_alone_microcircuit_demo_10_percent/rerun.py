from __future__ import print_function

from pacman103.core.spinnman.interfaces.transceiver import Transceiver
from pacman103.core.spinnman.interfaces.transceiver_tools.utility \
    import Utility
from pacman103.core.spinnman.scp import scamp

import os
import pickle
import sys

hostname = "192.168.240.1"
directory = "data_0.1_0.1"
binary_path = "binaries"
app_id = 30

txrx = Transceiver(hostname)

executable_targets_path = os.path.join(directory, "pickled_executable_targets")
executable_targets_file = open(executable_targets_path, "rb")
executable_targets = pickle.load(executable_targets_file)
executable_targets_file.close()

txrx.conn.set_iptag(1, "localhost", 17895)
targets = txrx.organise_targets(executable_targets)
total_processors = 0
for filename in targets.keys():
    print("Loading", filename, file=sys.stderr)
    chips = targets[filename]
    real_file = os.path.basename(filename)
    real_file = os.path.join(binary_path, filename)
    core_mask = 0
    for chip in chips:
        print("Loading on", chip, file=sys.stderr)
        processors = chips[chip]
        core_part_of_region = ""
        first = True
        for processor in processors:
            core_mask += processor
            if first:
                core_part_of_region += "{}".format(processor)
                first = False
            else:
                core_part_of_region += ",{}".format(processor)

            total_processors += 1

        (x, y) = chip.split(",")
        region = Utility.calculate_region_id(int(x), int(y))

        txrx.app_calls.app_load(real_file, region, core_part_of_region,
                                app_id)

        processors_ready = 0
        while processors_ready < total_processors:
            processors_ready = txrx.app_calls.app_signal(
                app_id, scamp.SIGNAL_COUNT, scamp.PROCESSOR_SYNC0)

txrx.app_calls.app_signal(app_id, scamp.SIGNAL_SYNC0)
