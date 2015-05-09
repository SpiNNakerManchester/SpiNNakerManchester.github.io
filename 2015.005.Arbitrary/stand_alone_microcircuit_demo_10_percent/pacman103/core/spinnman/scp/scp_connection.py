#
# DESCRIPTION
#   A simple implementation of the SpiNNaker command protocol.
#
# AUTHORS
#   Kier J. Dugan - (kjd1v07@ecs.soton.ac.uk)
#
# DETAILS
#   Created on       : 11 May 2012
#   Revision         : $Revision: 271 $
#   Last modified on : $Date: 2013-02-26 17:10:16 +0000 (Tue, 26 Feb 2013) $
#   Last modified by : $Author: kjd1v07 $
#   $Id: scp.py 271 2013-02-26 17:10:16Z kjd1v07 $
#
# COPYRIGHT
#   Copyright (c) 2012 The University of Southampton.  All Rights Reserved.
#   Electronics and Electrical Engingeering Group,
#   School of Electronics and Computer Science (ECS)
#

import math
import os
import socket
import struct

import scamp
from pacman103.core.spinnman.interfaces.iptag import IPTag
from pacman103.core.spinnman.scp.scp_message import SCPMessage
from pacman103.core.spinnman.scp.scp_error import SCPError
from pacman103.core.spinnman.scp.version_info import VersionInfo
from pacman103.core.spinnman.sdp.sdp_connection import SDPConnection
import logging
logger = logging.getLogger(__name__)
from pacman103.core.spinnman.interfaces.transceiver_tools.utility import Utility


# class that wraps up the SCP protocol
class SCPConnection (SDPConnection):
    """
    Builds on an :py:class:`SDPConnection` to support the SpiNNaker Command
    Protocol (SCP) which can interact with SC&MP and SARK.

    Example usage::

        conn = SCPConnection ('fiercebeast2', 17893)
        conn.select ('root')
        conn.set_iptag (0, 'localhost', 34521)
        conn.select (1)
        conn.write_mem_from_file (0x78000000, TYPE_WORD, 'myapp.aplx')
        conn.exec_aplx (0x78000000)

    It is possible to send user-specific :py:class:`SCPMessage`\ s if the target
    application uses the SCP packet format by simplying using the
    :py:meth:`send` and :py:meth:`receive` methods with :py:class:`SCPMessage`
    objects instead of :py:class:`SDPMessage`.  This class overrides both
    methods to ensure that this works correctly, which means that the *context
    manager* and *iterator* behaviours of :py:class:`SDPConnection` are
    automatically supported by :py:class:`SCPConnection`.

    .. note::

        :py:class:`SCPConnection` maintains an internal record of a *selected*
        processor and hence any :py:class:`SCPMessage`\ s sent will have their
        target members changed to reflect this internal record.

    .. seealso::

        - :py:class:`SCPMessage`
        - :py:class:`SDPConnection`
        - :py:class:`SDPMessage`

    """

    def __init__ (self, host, port=17893):
        """
        Constructs a new :py:class:`SCPConnection` object.

        :param str host: hostname of the remote SpiNNaker machine
        :param int port: port number to communicate through

        """

        # construct a normal SDP connection
        super (SCPConnection, self).__init__ (host, port)

        # intialise SCP members
        self._x     = 0
        self._y     = 0
        self._cpu   = 0
        self._node  = (self._x << 8) | self._y

        # initialise the sequence number counter
        self._seq = 0
        
        self.no_len_retries = 0
        self.no_timeout_retries = 0
        self.no_p2ptimeout_retries = 0
        
    def reset_retries(self):
        self.no_len_retries = 0
        self.no_timeout_retries = 0
        self.no_p2ptimeout_retries = 0
    
    def get_retries(self):
        return (self.no_timeout_retries, 
                self.no_p2ptimeout_retries,
                self.no_len_retries)

    def set_view(self, new_x, new_y, new_cpu, new_node):
        self._x = new_x
        self._y = new_y
        self._cpu = new_cpu
        self._node = new_node

    def __repr__ (self):
        """
        Custom representation for interactive programming -- overridden from
        SDPConnection.

        :return: string

        """

        return 'SCPConnection: {:s}[{:s}]:{:d}'.format (self.remote_hostname,
            self.remote_host_ip, self.remote_host_port)



    @property
    def selected_node_coords (self):
        """
        (X, Y) co-ordinates of the selected node in P2P space.

        """

        return (self._x, self._y)

    @selected_node_coords.setter
    def selected_node_coords (self, new_coords):
        (self._x, self._y) = new_coords
        self._node         = ((self._x & 0xFF) << 8) | (self._y & 0xFF)

    @property
    def selected_node (self):
        """
        Node P2P ID comprised of X|Y co-ordinates.

        """

        return self._node

    @selected_node.setter
    def selected_node (self, new_id):
        self._node = new_id
        (self._x, self._y) = ((new_id >> 8) & 0xFF, new_id & 0xFF)

    @property
    def selected_cpu (self):
        """
        Index of the selected CPU on the selected node.

        """

        return self._cpu

    @selected_cpu.setter
    def selected_cpu (self, new_cpu):
        self._cpu = new_cpu

    @property
    def selected_cpu_coords (self):
        """
        (X, Y, N) co-ordinates of the selected CPU (N) and node (X, Y).

        """

        return (self._x, self._y, self._cpu)

    @selected_cpu_coords.setter
    def selected_cpu_coords (self, new_coords):
        (self._x, self._y, self._cpu) = new_coords
        self._node = ((self._x & 0xFF) << 8) | (self._y & 0xFF)

    def receive (self, msg_type=SCPMessage):
        """
        Override from :py:class:`SDPConnection` to convert the socket data into
        an :py:class:`SCPMessage` object (or whichever is required).

        :param msg_type: :py:class:`SCPMessage`-derived class to unpack response
        :raises: socket.error, socket.timeout, struct.error

        """
        return super(SCPConnection, self).receive(msg_type)


    def send_scp_msg (self, msg, retries=10):
        """
        Dispatches the given packet and expects a response from the target
        machine.  Before the packet is sent, the destination co-ordinates and
        CPU index are altered to match the values internal to this class.

        :param SCPMessage msg: command packet to send to remote host
        :returns: :py:class:`SCPMessage` returned from the remote host
        :raises: SCPError

        """

        # update the message before sending
        msg.dst_cpu = self._cpu
        msg.dst_x   = self._x
        msg.dst_y   = self._y

        # get the response from the remote host
        sent_message = False
        resp = None
        self.next_seq_num()
        while not sent_message and retries > 0:
            try:
                self.send(msg)
                resp = self.receive()
                if ((resp.cmd_rc != scamp.RC_TIMEOUT) 
                        and (resp.cmd_rc != scamp.RC_P2P_TIMEOUT)
                        and (resp.cmd_rc != scamp.RC_LEN)):
                    sent_message = True
                else:
                    logger.debug("Warning - response was {}, retrying".format(
                            scamp.rc_to_string(resp.cmd_rc)))
                    if resp.cmd_rc == scamp.RC_TIMEOUT:
                        self.no_timeout_retries += 1
                    elif resp.cmd_rc == scamp.RC_P2P_TIMEOUT:
                        self.no_p2ptimeout_retries += 1
                    elif resp.cmd_rc == scamp.RC_LEN:
                        self.no_len_retries += 1
                    retries -= 1
            except socket.timeout as e:
                logger.debug("Warning - timeout waiting for response")
                retries -= 1
        if not sent_message:
            raise SCPError(0, "Failed to receive response after sending message")

        # deal with errors by making it someone else's problem!
        if resp.cmd_rc != scamp.RC_OK:
            raise SCPError(resp.cmd_rc, resp)
        else:
            return resp

    def version(self, retries=10):
        """
        Retreives the version information about the host operating system.

        :returns: version of OS in a class
        :raises:  SCPError

        """

        cmd_msg = SCPMessage (cmd_rc=scamp.CMD_VER)
        ver_msg = self.send_scp_msg (cmd_msg, retries=retries)

        # decode the payload into a usable struct
        return VersionInfo (ver_msg)

    def next_seq_num(self):
        """
        Generate a new sequence number for some of the SC&MP/SARK commands.

        :returns: int -- next sequence number

        """

        # mod 128 counter increment
        self._seq = (self._seq + 1) % 128
        return (2 * self._seq)

    def init_p2p_tables(self, cx, cy):
        """
        Configure the P2P tables on the remote SpiNNaker using the Manchester
        algorithm which superimposes a 2D co-ordinate space on the SpiNNaker
        fabric.

        :param int cx: width of the P2P space
        :param int cy: height of the P2P space

        """

        msg = SCPMessage (cmd_rc=scamp.CMD_P2PC)

        # generate a new sequence number
        seq = self.next_seq_num()

        # the following lines have been taken almost verbatim from ybug.
        # the comments state the following organisation but this is clearly no
        # longer the case:
        #   arg1 = 00 : 00 :   00   : seq num
        #   arg2 = cx : cy : addr x : addr y
        #   arg3 = 00 : 00 :   fwd  :  retry
        msg.arg1 = (0x003e << 16) | seq
        msg.arg2 = (cx << 24) | (cy << 16)
        msg.arg3 = 0x3ff8

        # send the command to SpiNNaker
        self.send_scp_msg (msg)

    def get_iptag_table_info (self):
        """
        Retrieve the number of fixed and transient tags available as well as
        the default timeout for all transient tags.

        :returns: fixed record count, transient record count, default timeout
        :raises:  SCPError

        """

        # build up the request according to the following formula:
        #   arg1 = 0 : command : 0 :    0
        #   arg2 = 0 :    0    : 0 : timeout
        #   arg3 = 0 :    0    : 0 :    0
        msg        = SCPMessage ()
        msg.cmd_rc = scamp.CMD_IPTAG
        msg.arg1   = scamp.IPTAG_TTO << 16
        msg.arg2   = 255                  # must be 16 or greater to be ignored
        msg.arg3   = 0
        resp_msg   = self.send_scp_msg (msg)

        # decode the response data (32bits) structured as follows:
        #   31:24 - max. number of fixed tags
        #   23:16 - max. number of transient tags
        #   15: 8 - reserved (0)
        #    7: 0 - transient timeout exponent
        if len (resp_msg.data) != 4:
            raise ValueError ("insufficient data received in response.")
        (ttoE, trans, fixed) =  struct.unpack ('Bx2B', resp_msg.data)

        # convert the timeout into seconds using the equation:
        #    timeout = 10ms * 2^(ttoE - 1)
        timeout = (1 << (ttoE - 1)) * 0.01

        return (fixed, trans, timeout)

    def set_transient_iptag_timeout (self, timeout):
        """
        Sets the timeout for all transient IP-tags on the target machine.

        :param float: timeout in *seconds*
        :raises: SCPError

        .. note::

            On the SpiNNaker node, all timeouts are stored in an exponential
            representation that limits the number of valid timeout durations to
            a small set.  Timeouts are calculated (from the node's perspective)
            as follows::

                timeout = 10ms * 2^(tto - 1)

            Hence timeout values passed into this function will be decomposed
            into ``tto`` in the above equation.

        """

        # convert the timeout into the exponent as explained above
        tto = int (math.ceil (math.log ((timeout / 0.01), 2))) + 1
        if tto >= 16:
            raise ValueError ("specific timeout is too large.")

        # set the new transient timeout
        #   arg1 = 0 : command : 0 :    0
        #   arg2 = 0 :    0    : 0 : timeout
        #   arg3 = 0 :    0    : 0 :    0
        msg        = SCPMessage ()
        msg.cmd_rc = scamp.CMD_IPTAG
        msg.arg1   = scamp.IPTAG_TTO << 16
        msg.arg2   = tto
        msg.arg3   = 0
        self.send_scp_msg (msg)

    def get_iptag (self, index):
        """
        Retrieve an IP-tag from the target SpiNNaker machine.

        :param int index: index in the IP-tag table.
        :returns:         IP tag data in a :py:class:`IPTag`
        :raises:          SCPError

        """

        # build up the request as follows:
        #   arg1 = 0 : command : 0 :  tag
        #   arg2 = 0 :    0    : 0 : count
        #   arg3 = 0 :    0    : 0 :   0
        msg        = SCPMessage ()
        msg.cmd_rc = scamp.CMD_IPTAG
        msg.arg1   = scamp.IPTAG_GET << 16 | index
        msg.arg2   = 1
        msg.arg3   = 0
        resp_msg   = self.send_scp_msg (msg)

        # deconstruct the returned data
        if len (resp_msg.data) != 16:
            raise ValueError ("insufficient data received in response.")
        (ip, mac, port, timeout, flags) = struct.unpack ('<4s6s3H',
            resp_msg.data)

        # format the IP and MAC addresses correctly
        ip  = '.'.join (['%d'   % ord (c) for c in ip])
        mac = ':'.join (['%02X' % ord (c) for c in mac])

        # return the data as a struct
        return IPTag(ip=ip, mac=mac, port=port, timeout=timeout/100.0,
            flags=flags, index=index)

    def new_iptag (self, host, port, timeout=0):
        """
        Add a new IP-tag record at the next available slot.

        :param str host:    hostname or IP address of destination
        :param int port:    port to use on destination
        :param int timeout: specific timeout to use, or 0 for default
        :returns:           record index in the IP-tag table
        :raises:            SCPError

        """

        return self.set_iptag (None, host, port, timeout)

    def set_iptag (self, index, host, port):
        """
        Set an IP-tag record at the required index.

        :param int index:   index in the IP-tag table
        :param str host:    hostname or IP address of destination
        :param int port:    port to use on destination
        :param int timeout: specific timeout to use, or 0 for default
        :returns:           record index in the IP-tag table
        :raises:            SCPError

        """

        # clamp the port and timeout to their appropriate ranges
        port    &= 0xFFFF

        # ensure that the given hostname is always an IP
        if host.lower () in ("localhost", "127.0.0.1", "."):
            host = self._sock.getsockname()[0]
        ip = socket.gethostbyname (host)

        # decompose the IP address into the component numbers and store in an
        # integer in REVERSE order so that it's correct after packing
        ip, segs = 0, ip.split ('.')
        if len (segs) != 4:
            raise ValueError ("IP address format is incorrect")
        for n, seg in enumerate (segs):
            ip |= (int (seg) << (8*n))

        msg = SCPMessage (cmd_rc=scamp.CMD_IPTAG)
        msg.arg1 = scamp.IPTAG_SET << 16 | (index & 0xFF)

        # the rest of the arguments follow the order:
        #   arg2 = port
        #   arg3 = IP
        msg.arg2 = port
        msg.arg3 = ip

        # fire off the packet
        self.send_scp_msg (msg)

    def clear_iptag (self, index):
        """
        Removes an IP-tag from the remote SpiNNaker.

        :param int index: index to remove from the table
        :raises:          SCPError

        """

        # build up the request as follows:
        #   arg1 = 0 : command : 0 : tag
        #   arg2 = 0 :    0    : 0 :  0
        #   arg3 = 0 :    0    : 0 :  0
        msg        = SCPMessage ()
        msg.cmd_rc = scamp.CMD_IPTAG
        msg.arg1   = (scamp.IPTAG_CLR << 16) | index

        # fire off the command
        self.send_scp_msg (msg)

    def get_all_iptags (self):
        """
        Retrieves all registered IP-tags from the target SpiNNaker machine.

        :returns: list of :py:class:`Struct`\ s containing IP-tag information
        :raises:  SCPError

        """

        iptags = []

        # get the total number of possible IP tag records
        fixed, trans, timeout = self.get_iptag_table_info ()

        # iterate over the possibilities
        for i in xrange (fixed + trans):
            iptag = self.get_iptag (i)

            # add valid records to the list
            if iptag.flags & scamp.IPTAG_VALID:
                iptags.append (iptag)

        # return whatever we found (possibly an empty list)
        return iptags



    def set_leds (self, led1=scamp.LED_NO_CHANGE, led2=scamp.LED_NO_CHANGE,
            led3=scamp.LED_NO_CHANGE, led4=scamp.LED_NO_CHANGE):
        """
        Changes the state of the LEDs of the target SpiNNaker node.

        :param int led1: action for LED 1
        :param int led2: action for LED 2
        :param int led3: action for LED 3
        :param int led4: action for LED 4
        :raises: SCPError

        Each ``ledN`` parameter may be given one of four values from the SC&MP
        definitions: ``LED_NO_CHANGE``, ``LED_INVERT``, ``LED_OFF``, or
        ``LED_ON``.

        """

        # LED control signals exist only in the lowest byte of arg1
        msg        = SCPMessage ()
        msg.cmd_rc = scamp.CMD_LED
        msg.arg1   = (led4 << 6) | (led3 << 4) | (led2 << 2) | led1
        self.send_scp_msg (msg)










