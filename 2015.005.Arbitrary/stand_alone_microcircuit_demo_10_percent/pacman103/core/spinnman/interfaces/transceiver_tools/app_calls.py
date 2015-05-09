'''
application specific commands are stored here for clarity
'''

from pacman103.core.spinnman.interfaces.transceiver_tools.utility import Utility
from pacman103.core.spinnman.scp.scp_message import SCPMessage
from pacman103.core.spinnman.scp import scamp
from pacman103.core import exceptions
import logging
import struct
logger = logging.getLogger(__name__)


class AppCalls(object):
    def __init__(self, transceiver):
        self._x = 0
        self._y = 0
        self._cpu = 0
        self._node = (self._x << 8) | self._y
        self.transceiver = transceiver
        self.signal_states = {0: 'init', 1: 'pwrdn', 2: 'stop', 3: 'start',
                              4: 'sync0', 5: 'sync1', 6: 'pause', 7: 'cont',
                              8: 'exit', 9: 'timer', 10: 'usr0', 11: 'usr1',
                              12: 'usr2', 13: 'usr3', 16: 'or', 17: 'and',
                              18: 'count'}
        self.states = {0: 'dead', 1: 'pwrdn', 2: 'rte', 3: 'wdog', 4: 'init',
                       5: 'ready', 6: 'c_main', 7: 'run', 8: 'sync0',
                       9: 'sync1', 10: 'pause', 11: 'exit', 15: 'idle'}
        self.sig_type = {'init': 2, 'pwrdn': 2, 'stop': 2, 'start': 2,
                         'sync0': 2, 'sync1': 0, 'pause': 0, 'cont': 0,
                         'exit': 2, 'timer': 0, 'usr0': 0, 'usr1': 0,
                         'usr2': 0, 'usr3': 0, 'or': 1, 'and': 1, 'count': 1}

        self.spinnaker_utility = Utility()

        #self.states = {'dead': 0, 'pwrdn' :1, 'rte': 2, 'wdog': 3,
           #            'init': 4, 'ready': 5, 'c_main': 6, 'run': 7,
          #             'sync0': 8, 'sync1': 9, 'pause': 10, 'exit': 11,
          #             'idle': 15}
        #self.signal_states = {'init': 0, 'pwrdn': 1, 'stop': 2, 'start': 3,
                              #'sync0': 4, 'sync1': 5, 'pause': 6, 'cont': 7,
                             # 'exit': 8, 'timer': 9, 'usr0': 10, 'usr1': 11,
                             # 'usr2': 12, 'usr3': 13, 'or': 16, 'and': 17,
                             # 'count': 18}


    def set_view(self, new_x, new_y, new_cpu, new_node):
        self._x = new_x
        self._y = new_y
        self._cpu = new_cpu
        self._node = new_node

    def app_load(self, filename, region, cores, app_id, flags=None):
        '''
        loads a .aplx file onto a collection of cores based off the region given
        '''
        logger.debug("Loading %s to region %s, cores %s, appid %s", filename,
                 region, cores, app_id)
        app_flags = 0

        if flags != None and flags == "wait":
            app_flags |= 1

        region = self.spinnaker_utility.parse_region(region, self._x, self._y)

        mask = self.spinnaker_utility.parse_cores(cores)
        data = self.spinnaker_utility.read_file(filename)

        try:
            self.transceiver.packet_calls.flood_fill(data, region,
                                                     mask, app_id,
                                                     app_flags)
        except exceptions.SpinnManException as e:
            print "failed to flood fill the machine due " \
                  "to {}".format(e.message)


    def app_signal(self, app_id, signal_id, state_id=None, x=None,
                   y=None, range=None):
        '''
        method that allows signals to be polled and sent to areas of a board
        '''
        #define the region
        region = ""
        if(x is None and y is None):
            region = "all"

        if signal_id not in self.signal_states:
            raise exceptions.SpinnManException("signal definition does not "
                                               "exist for {}. List is {}"
                                               .format(signal_id,
                                                       self.signal_states))
        region = self.spinnaker_utility.parse_region(region, x, y)

        #locate signal name id
        signal = self.signal_states[signal_id]

        #locate state id
        state = None
        if signal_id >= 16:
            if state_id is not None:
                if state_id in self.states:
                    state = self.states[state_id]
                else:
                    raise exceptions.SpinnManException("No state with that id")
            else:
                raise exceptions.SpinnManException("state was defined as None "
                                                   "when using a and/or/count "
                                                   "signal")

        #locate type of signal
        signal_type = self.sig_type[signal]

        #parse the apps for a app mask
        app_mask = self.spinnaker_utility.parse_apps(app_id, range)
        mask = int(region) & 0xffff
        data = (app_mask << 8) + app_id

        #if signal type is 1
        if signal_type == 1:
            level = (region >> 16) & 3
            op, mode = 2, 2

            #if signal is a and/or/count
            if signal_id >= 16:
                op = 1
                mode = signal_id - 16
                data += (level << 26) + (op << 22) + (mode << 20)
                if op == 1:
                    data += state_id << 16
                if op != 1:
                    data += signal_id << 16
               # logger.debug("Level {} op {} mode {}".format(level, op, mode))
        else:
            data += signal_id << 16

       # logger.debug("Type {} data {} mask {}".format(signal_type, data, mask))
       # logger.debug("Region {} signal {} state {}".format(region, signal, state))

        #send scp message and catch the return data
        msg = SCPMessage(cmd_rc=scamp.CMD_SIG)
        msg._arg1 = signal_type
        msg._arg2 = data
        msg._arg3 = mask
        return_data = self.transceiver.conn.send_scp_msg(msg).data

        # if the signal requires a repsonse, output resposne and return it
        if signal_type == 1:
            r = struct.unpack("<I", return_data)[0]
            if signal_id == 18: #count
                #logger.debug("count {}".format(r))
                return r
           # else:
                #logger.debug("mask {}".format(r))
        return 0



    def app_fill(self):
        pass

    def app_stop(self):
        pass

    def exec_app_start(self, start_addr, cpu_mask):
        """
        Simultaneously executes APLX images on several processors in the target
        SpiNNaker node.

        :param int start_addr: memory address of the APLX image
        :param int cpu_mask: bit-mask of processors on which to execute the image
        :raises: SCPError

        ``cpu_mask`` is an integer *mask* where each bit corresponds to a
        processor on the target SpiNNaker node, i.e. bit N implies that the
        program should be executed on processor N.

        .. warning::

            The monitor processor **is** included in the ``cpu_mask`` which can
            lead to errors if the APLX image was not designed to run on the
            monitor pacman.

        """

        # simple packet:
        #   arg1 = address of program in memory
        #   arg2 = cpu mask - each bit corresponds to a pacman in the chip
        #   arg3 = unused
        msg        = SCPMessage()
        msg.cmd_rc = scamp.CMD_AS
        msg.arg1   = start_addr
        msg.arg2   = cpu_mask
        self.transceiver.conn.send_scp_msg(msg)

    def exec_aplx (self, start_addr):
        """
        Executes an APLX image on the target SpiNNaker node.

        :param int start_addr: memory address of the APLX image
        :raises: SCPError

        """

        # simple packet:
        #   arg1 = address of "table" (i.e. program start in SDRAM)
        #   arg2 = unused parameter - must be 0
        #   arg3 = unused
        msg        = SCPMessage ()
        msg.cmd_rc = scamp.CMD_APLX
        msg.arg1   = start_addr
        self.transceiver.conn.send_scp_msg (msg)


