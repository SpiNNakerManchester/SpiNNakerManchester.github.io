from __future__ import print_function

from pacman103.core.spinnman.interfaces.transceiver import Transceiver
from pacman103.core.process_bar import ProgressBar
from pacman103.core.spinnman.scp import scamp
from pacman103.core.spinnman.scp import boot

import os
import pickle
import struct
import sys
import time

hostname = "192.168.240.1"
version = 5
directory = "data_0.1_0.1"

txrx = Transceiver(hostname)
while True:
    try:
        print("Trying to get version")
        version = txrx.conn.version(retries=3)
        print("Version =", version.desc)
        break
    except:
        print("Couldn't get version, rebooting")
        boot_file = txrx.checkfile("scamp-130.boot")
        struct_file = txrx.checkfile("sark-130.struct")
        config_file = txrx.checkfile("spin{}.conf".format(5))
        boot.boot(hostname, boot_file, config_file, struct_file)
        time.sleep(2.0)

load_targets_path = os.path.join(directory, "pickled_load_targets")
mem_write_targets_path = os.path.join(directory, "pickled_mem_write_targets")
load_targets_file = open(load_targets_path, "rb")
load_targets = pickle.load(load_targets_file)
load_targets_file.close()
mem_write_targets_file = open(mem_write_targets_path, "rb")
mem_write_targets = pickle.load(mem_write_targets_file)
mem_write_targets_file.close()

print("Loading data", file=sys.stderr)
load_progress = ProgressBar(len(load_targets))
for target in load_targets:
    txrx.select(target.x, target.y, target.p)
    filename = os.path.basename(target.filename)
    filename = os.path.join(directory, filename)
    txrx.memory_calls.write_mem_from_file(target.address, scamp.TYPE_WORD,
                                          filename)
    load_progress.update()
load_progress.end()

print("Writing memory", file=sys.stderr)
mem_progress = ProgressBar(len(mem_write_targets))
for target in mem_write_targets:
    txrx.select(target.x, target.y, target.p)
    txrx.memory_calls.write_mem(target.address, scamp.TYPE_WORD,
                                struct.pack("I", target.data))
    mem_progress.update()
mem_progress.end()
