import struct

class SDPMessage (object):
    """
    Wraps up an SDP message that may be sent or received to/from a SpiNNaker
    using a :py:class:`SDPConnection`.

    Typical usage::

        conn         = SDPConnection ('fiercebeast2', 17892)
        msg          = SDPMessage ()
        msg.dst_cpu  = 1
        msg.dst_port = 7
        msg.data     = "Hello!"
        conn.send (msg)

    Only a small number of fields are used for SDP messages:

        ``flags`` (8 bits)
            Amongst other things, determines whether the packet commands a
            response or not

        ``tag`` (8 bits)
            IP tag to use, or the IP used.

        ``dst_cpu`` (5 bits)
            Target processor on target node (0-17)

        ``dst_port`` (3 bits)
            Port on target processor (0-7)

        ``src_cpu`` (5 bits)
            Originating processor on source node (0-17)

        ``src_port`` (3 bits)
            Port on source processor (0-7)

        ``dst_x`` and ``dst_y`` (both 8 bits)
            (X, Y) co-ordinates of target node

        ``src_x`` and ``src_y`` (both 8 bits)
            (X, Y) co-ordinates of initiating node

        ``data`` (variable length)
            Up to 272 bytes of payload data

    .. note::

        Although :class:`SDPMessage` is typically used in conjunction with the
        :class:`SDPConnection` class, this is not a requirement.  Calling
        :func:`str` on an :class:`SDPMessage` object will encode the contents
        as a string, and calling :py:meth:`~SDPMessage.from_string` will perform
        the reverse.

    """

    def __init__ (self, packed=None, **kwargs):
        """
        Constructs a new :py:class:`SDPMessage` object with either default
        values or those provided.

        :param packed: encoded packet data
        :type packed:  string or None
        :param kwargs: keyword arguments providing initial values

        .. note::

            If neither ``packed`` nor ``kwargs`` are provided than internal
            default values will be used.

        """

        # sizeof(sdp_hdr_t) == 8 in SC&MP/SARK -- used for the size calculation
        self._sizeof_hdr = 8

        if packed is not None:
            self.from_string (packed)
        else:
            self.flags    = 0x87
            self.tag      = 0xFF
            self.dst_cpu  =    0
            self.dst_port =    1
            self.src_cpu  =   31
            self.src_port =    7
            self.dst_x    =    0
            self.dst_y    =    0
            self.src_x    =    0
            self.src_y    =    0
            self.data     = ''

        # use given values if possible
        if kwargs:
            self.from_dict (kwargs)

    def _pack_hdr (self):
        """
        Constructs a string containing *only* the SDP header.

        :returns: header encoded as a string

        """

        # generate source and destination addresses
        src_proc = ((self.src_port & 7) << 5) | (self.src_cpu & 31)
        dst_proc = ((self.dst_port & 7) << 5) | (self.dst_cpu & 31)
        src_addr = ((self.src_x & 0xFF) << 8) | (self.src_y & 0xFF)
        dst_addr = ((self.dst_x & 0xFF) << 8) | (self.dst_y & 0xFF)

        # pack the header
        packed = struct.pack ('< 6B 2H', 8, 0, self.flags, self.tag, dst_proc,
            src_proc, dst_addr, src_addr)

        return packed

    def __str__ (self):
        """
        Constructs a string that can be sent over a network socket using the
        member variables.

        :returns: encoded string

        """

        # return the full packet
        return self._pack_hdr () + self.data

    def __len__ (self):
        """
        Determines the length of the SDP message represented by this class.

        :returns: length of the data in this object

        """

        return self._sizeof_hdr + len (self.data)

    def _unpack_hdr (self, packed):
        """
        Reconstructs only an SDP header from ``packed`` and returns what is
        assumed to be payload.

        :param str packed: packed data to decode
        :returns:          dictionary of header fields, payload

        """

        # divide the data into the header and the payload
        pkt, header, payload = {}, packed[:10], packed[10:]

        # unpack the header
        (pkt['flags'], pkt['tag'], dst_proc, src_proc, dst_addr,
            src_addr) = struct.unpack ('< 2x 4B 2H', header)

        # unmap the tightly packed bits
        pkt['src_port'], pkt['src_cpu'] = src_proc >> 5, src_proc & 0x1F
        pkt['dst_port'], pkt['dst_cpu'] = dst_proc >> 5, dst_proc & 0x1F
        pkt['src_x'],    pkt['src_y']   = src_addr >> 8, src_addr & 0xFF
        pkt['dst_x'],    pkt['dst_y']   = dst_addr >> 8, dst_addr & 0xFF

        # return the unpacked header and the payload
        return pkt, payload


    def from_string (self, packed):
        """
        Deconstructs the given string and sets the member variables accordingly.

        :param str packed: packed data to process
        :raises: :py:class:`struct.error`

        """

        # unpack the header and the payload
        hdr, payload = self._unpack_hdr (packed)

        # merge the fields and store the payload
        self.from_dict (hdr)
        self.data = payload

    def from_dict (self, map):
        """
        Updates the SDPMessage object from the given key-value map of valid
        fields.

        :param dict map: valid SDP fields

        """

        for k, v in map.iteritems ():
            setattr (self, k, v)