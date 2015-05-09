from pacman103.core.spinnman.interfaces.transceiver_tools.utility import Utility
import math
import sys
import logging
from pacman103.core.spinnman.scp import scamp
from pacman103.core.spinnman.scp.scp_message import SCPMessage
logger = logging.getLogger(__name__)

#constants
NN_CMD_FFS = 6
NN_CMD_FFE = 15
BLOCK_SIZE = 256

class PacketCalls(object):

    def __init__(self, transceiver):
        self._x = 0
        self._y = 0
        self._cpu = 0
        self._node = (self._x << 8) | self._y
        self.transceiver = transceiver
        self.nn_id = 0

    def set_view(self, new_x, new_y, new_cpu, new_node):
        self._x = new_x
        self._y = new_y
        self._cpu = new_cpu
        self._node = new_node

    def flood_fill(self, buf, region, mask, app_id,
                   app_flags, base=0x67800000):

        num_bytes = len(buf)
        blocks = int(num_bytes / BLOCK_SIZE)
        if (num_bytes % BLOCK_SIZE) != 0:
          blocks += 1
          
        logger.debug("Bytes %u blocks %u" % (num_bytes, blocks))
   
        sfwd, srty = 0x3f, 0x18# Forward, retry parameters

        ff_id = self.next_id()

        fr = (sfwd << 8) + srty# Pack up fwd, rty
        sfr = (1 << 31) + fr# Bit 31 says allocate ID on Spin

        filename = (NN_CMD_FFS << 24) + (ff_id << 16) + (blocks << 8) + 0
        data = region

        self.nnp(filename, data, sfr)

        #send FFD data

        ptr = 0

        for block in range(blocks):
            end = ptr + BLOCK_SIZE
            data = buf[ptr:end]

            word_size = (len(data) / 4) - 1 #convert to word size (why -1?)
            arg1 = (sfwd << 24) + (srty << 16) + (0 << 8) + ff_id #??
            arg2 = (0 << 24) + (block << 16) + (word_size << 8) + 0 #??

            msg = SCPMessage(cmd_rc=scamp.CMD_FFD)
            #initlise values
            msg.arg1 = arg1
            msg.arg2 = arg2
            msg.arg3 = base
            msg.payload = data

            self.transceiver.conn.send_scp_msg(msg)
            #update pointer to next block
            base += BLOCK_SIZE
            ptr += BLOCK_SIZE

        # send FFE packet
        filename = (NN_CMD_FFE << 24) + (0 << 16) + (0 << 8) + ff_id # const
        data = (app_id << 24) + (app_flags << 18) + (mask & 0x3ffff)
        self.nnp(filename, data, fr)


    def nnp(self, key, data, sfr):
        msg = SCPMessage(cmd_rc=scamp.CMD_NNP)
        #initlise values
        msg._arg1 = key
        msg._arg2 = data
        msg._arg3 = sfr
        self.transceiver.conn.send_scp_msg(msg)

    def next_id(self):
        new_id = self.nn_id + 1
        if new_id > 127:
            new_id = 1
        self.nn_id = new_id
        return 2 * new_id



