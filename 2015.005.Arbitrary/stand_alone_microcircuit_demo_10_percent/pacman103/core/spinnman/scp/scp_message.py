import struct
from pacman103.core.spinnman.sdp.sdp_message import SDPMessage

class SCPMessage (SDPMessage):
    """
    Builds on :py:class:`SDPMessage` by adding the following fields to support
    SCP messages:

        ``cmd_rc`` (16 bits)
            *command* on outgoing packets and *response code* on incoming
            packets

        ``seq`` (16 bits)
            sequence code -- not used for every command type

        ``arg1``, ``arg2``, ``arg3`` (all 32 bits)
            optional word data at the start of the payload that may be ignored
            if ``raw_data`` is used directly

        ``payload`` (variable length)
            optional data field that appears *after* the optional arguments in
            the SCP payload

        ``data`` (variable length)
            SCP packet payload *including* the optional word data fieelds.

        ``has_args`` (boolean)
            indicates whether the word data fields are used or not

    Usage::

        conn         = SCPConnection ('fiercebeast2')
        msg          = SCPMessage ()
        msg.cmd_rc   = scamp.CMD_VER
        msg.has_args = False
        response     = conn.send (msg)

    .. seealso::

        - :py:class:`SCPConnection`
        - :py:class:`SDPConnection`
        - :py:class:`SDPMessage`

    """

    def __init__ (self, packed=None, **kwargs):
        """
        Contructs a new :py:class:`SCPMessage` object -- overloaded from base
        class to add new members.

        :param packed: encoded packet data
        :type packed:  string or None
        :param kwargs: keyword arguments providing initial values

        """

        # (sizeof(sdp_hdr_t) + 2*sizeof(uint16_t) == 12 in SC&MP/SARK -- used
        # for the size calculation
        self._sizeof_hdr = 12

        # call base class
        super (SCPMessage, self).__init__ ()

        # default initialise new members before calling the base constructor
        self.dst_port = 0  # override from base class for command port
        self.cmd_rc   = 0
        self.seq      = 0
        self.arg1     = 0
        self.arg2     = 0
        self.arg3     = 0
        self.payload  = ''
        self.data     = ''
        self.has_args = True

        # handle the packed data and keyword arguments after default init
        if packed is not None:
            self.from_string (packed)
        if kwargs:
            self.from_dict (kwargs)

    def _pack_hdr (self):
        """
        Overloaded from base class to pack the extra header fields.

        """

        # pack the two compulsory SCP fields and append them to the SDP header
        scp_packed = struct.pack ('<2H', self.cmd_rc, self.seq)

        return super (SCPMessage, self)._pack_hdr () + scp_packed

    def _unpack_hdr (self, packed):
        """
        Overloaded from base class to unpack the extra header fields.

        :param str packed: encoded string

        """

        # get the SDP header from the base class
        pkt, payload = super (SCPMessage, self)._unpack_hdr (packed)

        # strip 4 bytes from the payload to decode the SCP compulsory fields
        scp_hdr, payload = payload[:4], payload[4:]
        (pkt['cmd_rc'], pkt['seq']) = struct.unpack ('<2H', scp_hdr)

        return pkt, payload

    @property
    def arg1 (self):
        """
        Optional integer argument 1.

        """

        return self._arg1

    @arg1.setter
    def arg1 (self, value):
        self._arg1    = value
        self.has_args = True

    @property
    def arg2 (self):
        """
        Optional integer argument 2.

        """

        return self._arg2

    @arg2.setter
    def arg2 (self, value):
        self._arg2    = value
        self.has_args = True

    @property
    def arg3 (self):
        """
        Optional integer argument 3.

        """

        return self._arg3

    @arg3.setter
    def arg3 (self, value):
        self._arg3    = value
        self.has_args = True

    @property
    def data (self):
        """
        Optional payload for the :py:class:`SCPMessage` object -- automatically
        packs the word arguments and variable-length data into a single value.

        """

        if self.has_args:
            _data  = struct.pack ('<3I', self.arg1, self.arg2, self.arg3)
            _data += self.payload
        else:
            _data = self._data

        return _data

    @data.setter
    def data (self, value):
        """
        Optional payload for the message -- automatically unpacks the word
        arguments if there is sufficient space to do so.

        :param str value: payload to unpack

        """

        if len (value) >= 12:
            self.has_args = True
            (self.arg1, self.arg2, self.arg3) = struct.unpack ('<3I',
                value[:12])
            self.payload = value[12:]
        else:
            self.has_args = False
            self._data = value

