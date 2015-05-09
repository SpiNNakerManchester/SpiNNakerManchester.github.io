#
# DESCRIPTION
#   Very bare metal SDP library containing all the constants from ybug and
#   spinnaker.h and a pair of functions capable of building and parsing SDP
#   packets received from a socket.
#
#   Included for backwards compatibility.
#
# AUTHORS
#   Kier J. Dugan - (kjd1v07@ecs.soton.ac.uk)
#
# DETAILS
#   Created on       : 16 December 2011
#   Revision         : $Revision: 198 $
#   Last modified on : $Date: 2012-07-18 17:51:12 +0100 (Wed, 18 Jul 2012) $
#   Last modified by : $Author: kjd1v07 $
#   $Id: legacy.py 198 2012-07-18 16:51:12Z kjd1v07 $
#
# COPYRIGHT
#   Copyright (c) 2011 The University of Southampton.  All Rights Reserved.
#   Electronics and Electrical Engingeering Group,
#   School of Electronics and Computer Science (ECS)
#

#imports
import struct
import scamp


# constants
__all__ = ['build', 'parse']


# functions
def build (has_args=True, **kwargs):
    """
    Takes a set of keyword arguments and uses them to construct an SCP packet
    that can be sent to SpiNNaker using a network connection.
    
    :param bool has_args: True to make arg1, arg2 and arg3 valid
    :param kwargs:        keyword arguments to include in the packet
    
    .. warning::
        
        This function is now considered deprecated, use :class:`SDPMessage` and
        :class:`SDPConnection` instead.
    
    """
    
    params = {
        'flags'     :          0x87,
        'tag'       :          0xFF,
        'dst_cpu'   :             0,
        'dst_port'  :             0,
        'src_cpu'   :            31,    
        'src_port'  :             7,
        'dst_x'     :             0,
        'dst_y'     :             0,
        'src_x'     :             0,
        'src_y'     :             0,
        'cmd_rc'    : scamp.CMD_VER,
        'seq'       :             0,
        'arg1'      :             0,
        'arg2'      :             0,
        'arg3'      :             0,
        'data'      :            '',
    }
    params.update (kwargs)
    
    # generate source and destination addresses
    src_proc = ((params['src_port'] & 7) << 5) | (params['src_cpu'] & 31)
    dst_proc = ((params['dst_port'] & 7) << 5) | (params['dst_cpu'] & 31)
    src_addr = ((params['src_x'] & 0xFF) << 8) | (params['src_y'] & 0xFF)
    dst_addr = ((params['dst_x'] & 0xFF) << 8) | (params['dst_y'] & 0xFF)

    # create the packet
    packet = struct.pack ('< 6B 2H 2H', 8, 0, params['flags'], params['tag'],
        dst_proc, src_proc, dst_addr, src_addr, params['cmd_rc'], params['seq'])
    
    # all packets except tubotron messages have three optional int arguments
    #if params['cmd_rc'] != CMD_TUBE:
    if has_args:
        # add integer arguments
        packet += struct.pack ('<3L', params['arg1'], params['arg2'],
            params['arg3'])
        
        # trim data to 256 bytes in length
        params['data'] = params['data'][:256]
    else:
        # tube messages consider the 3 ints as normal data
        params['data'] = params['data'][:268] # 268 = 256 + 3*4
    
    # add the data and return the packet
    packet += params['data']
    return packet

def parse (data, has_args=True):
    """
    Deconstructs a string of byte data received from a network channel into
    a dictionary of ``key=value`` pairs.
    
    :param str data:      data to deconstruct
    :param bool has_args: True if arg1, arg2 and arg3 should be considered
    
    .. warning::
        
        This function is now considered deprecated, use :class:`SDPMessage` and
        :class:`SDPConnection` instead.
    
    """
    
    packet = {}
    
    # separate the header at the data
    hdr, packet['raw_data'] = data[:14], data[14:]
    
    # deconstruct the header only
    (packet['flags'], packet['tag'], dst_proc, src_proc, dst_addr, src_addr,
        packet['cmd_rc'], packet['seq']) = struct.unpack ('< 2x 4B 2H 2H', hdr)

    # process the data if necessary
    if has_args and packet['raw_data']:
        (packet['arg1'], packet['arg2'], packet['arg3']) = \
            struct.unpack ('< 3L', packet['raw_data'][:12])
        packet['data'] = packet['raw_data'][12:]
    else:
        (packet['arg1'], packet['arg2'], packet['arg3']) = (0L, 0L, 0L)
        packet['data'] = packet['raw_data']
    
    # process address information
    packet['src_port'], packet['src_cpu'] = src_proc >> 5, src_proc & 0x1F
    packet['dst_port'], packet['dst_cpu'] = dst_proc >> 5, dst_proc & 0x1F
    packet['src_x'],    packet['src_y']   = src_addr >> 8, src_addr & 0xFF
    packet['dst_x'],    packet['dst_y']   = dst_addr >> 8, dst_addr & 0xFF
    
    return packet
    
