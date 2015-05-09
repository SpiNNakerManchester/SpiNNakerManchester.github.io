import numpy

from pacman103.core.spinnman.scp.scp_connection import SCPConnection
from pacman103.core.spinnman.interfaces.transceiver_tools.app_calls import AppCalls
from pacman103.core.spinnman.interfaces.transceiver_tools.memory_calls import MemoryCalls
from pacman103.core.spinnman.interfaces.transceiver_tools.packet_calls import PacketCalls
from pacman103.core.spinnman.interfaces.transceiver_tools.utility import Utility
from pacman103.core.spinnman.scp import scamp
import sys


import logging
import os
from pacman103.core.spinnman.interfaces import boot_files
logger = logging.getLogger(__name__)


class Transceiver(object):
    """
    A Transceiver is instantiated by a
    :py:func:`pacman103.pacman.control.Controller` object in order to communicate
    with a SpiNNaker board. The Transceiver class is simply a wrapper around the
    :py:mod:`pacman103.scp` module, which does the actual interfaces over
    Ethernet. An instance of the class maintains a SCP connection to a machine,
    through which all interfaces takes place.

    :param string hostname:
        hostname of the SpiNNaker machine on which the simulation is to be run.
    """

    def __init__(self, hostname, port=17893):
        self.conn = SCPConnection(hostname, port)
        self.app_calls = AppCalls(self)
        self.memory_calls = MemoryCalls(self)
        self.packet_calls = PacketCalls(self)
        self._x = 0
        self._y = 0
        self.utility = None

    def read_memory(self, x, y, p, a, l, dtype):
        """
        Read memory from the SpiNNaker machine.

        :param int x: x-chip-coordinate.
        :param int y: y-chip-coordinate.
        :param int p: processor ID.
        :param int a: target load address.
        :param int l: length of data to read (bytes).
        :param numpy.dtype dtype:
            datatype of the returned numpy array (e.g. numpy.int32)

        :returns: numpy.ndarray containing the requested memory.
        """
        self.select(x, y, p)
        memory = self.memory_calls.read_mem(a, scamp.TYPE_WORD, l)
        memory = numpy.fromstring(memory, dtype=dtype)

        return memory

    def organise_targets(self, targets):
        '''
        method that takes the targets and converts them into a list of chip scoped
        targets where each entry contains the chip
        '''
        organised_targets = dict()
        for target in targets:
            filename = "{},{}".format(target.targets[0]['x'], target.targets[0]['y'])
            proc = target.targets[0]['p']
            if organised_targets.has_key(target.filename):
                chip_collection = organised_targets.get(target.filename)
                if filename in chip_collection:
                    chip_collection[filename].append(proc)
                else:
                    chip_collection[filename] = [proc]
            else:
                #add with the chip definition
                chip_collection = dict()
                chip_collection[filename] = [proc]
                organised_targets[target.filename] = chip_collection
        return organised_targets

    def checkfile(self, test_file):
        real_file = test_file
        if not os.path.isfile(real_file):
            directory = os.path.dirname(boot_files.__file__)
            real_file = os.path.join(directory, real_file)
        if not os.path.isfile(real_file):
            print "File %s not found" % test_file
            sys.exit(3)
        return real_file

    def select (self, *args):
        """
        Select the target node and processor.

        :param args: variadic argument (usage below)
        :raises:     ValueError

        This function has the following calling conventions:

            ``conn.select ('root')``
                Short-hand to select node (0, 0, 0)

            ``conn.select (N)``
                Selects processor N on the currently selected node

            ``conn.select (X, Y)``
                Selects processor 0 on node (``X``, ``Y``)

            ``conn.select (X, Y, N)``
                Selects processor ``N`` on node (``X``, ``Y``)

        """

        # extract the arguments
        if len (args) == 1 and type (args[0]) == str and args[0] == "root":
            (x, y, cpu) = (0, 0, 0)
        elif len (args) == 1 and type (args[0]) == int:
            (x, y, cpu) = (self._x, self._y, args[0])
        elif len (args) == 2:
            (x, y, cpu) = (args[0], args[1], 0)
        elif len (args) == 3:
            (x, y, cpu) = args
        else:
            raise ValueError ("invalid arguments given for SCPConnection."
                "select call.")

        # make sure that the variables are all ints
        if type (x) != int or type (y) != int or type (cpu) != int:
            raise ValueError ("invalid argument types given expecting ints or "
                "a single string 'root'.")

        # save the variables
        self.app_calls.set_view(x & 0xFF, y & 0xFF, cpu, (self._x << 8) | self._y)
        self.memory_calls.set_view(x & 0xFF, y & 0xFF, cpu, (self._x << 8) | self._y)
        self.packet_calls.set_view(x & 0xFF, y & 0xFF, cpu, (self._x << 8) | self._y)
        self.conn.set_view(x & 0xFF, y & 0xFF, cpu, (self._x << 8) | self._y)
        self._x = x & 0xFF
        self._y = y & 0xFF
