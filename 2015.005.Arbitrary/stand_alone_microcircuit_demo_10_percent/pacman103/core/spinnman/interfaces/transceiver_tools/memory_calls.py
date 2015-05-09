from pacman103.core.spinnman.interfaces.transceiver_tools.utility import Utility
from pacman103.core.spinnman.scp.scp_message import SCPMessage
from pacman103.core.spinnman.scp import scamp
import os


class MemoryCalls(object):

    def __init__(self, transceiver):
        self._x = 0
        self._y = 0
        self._cpu = 0
        self._node = (self._x << 8) | self._y
        self.transceiver = transceiver

    def set_view(self, new_x, new_y, new_cpu, new_node):
        self._x = new_x
        self._y = new_y
        self._cpu = new_cpu
        self._node = new_node


    def write_mem (self, start_addr, type, data):
        """
        Uploads data to a target SpiNNaker node at a specific memory location.

        :param int start_addr: base address for the uploaded data
        :param int type:       one of ``TYPE_BYTE``, ``TYPE_HALF``, or
                               ``TYPE_WORD`` to indicate element type
        :param str data:       string of data to upload
        :raises:               SCPError

        """

        msg = SCPMessage (cmd_rc=scamp.CMD_WRITE, arg3=type)

        # confirm the data length is aligned to the appropriate boundary
        self._check_size_alignment(type, len (data))

        # upload the data in maximum-sized chunks
        addr = start_addr
        for chunk in self.gen_slice(data, scamp.SDP_DATA_SIZE):
            # build up the packet as follows:
            #   arg1 = start address
            #   arg2 = chunk length
            #   arg3 = element size
            msg.arg1    = addr
            msg.arg2    = len (chunk)
            msg.payload = chunk
            self.transceiver.conn.send_scp_msg(msg)

            # increment the address pointer
            addr += len (chunk)



    def gen_slice (self, seq, length):
        """
        Generator function to slice a container into smaller chunks.

        :param seq:        iterable container
        :param int length: length of each slice of ``seq``
        :returns:          appropriate slice of ``seq``

        Example::

            >>> for slice in self.gen_slice ("Hello!", 3):
            ...     print slice
            Hel
            lo!

        """

        start = 0
        end   = length

        # iterate over the container
        while True:
            # extract a new segment and update the slice bounds
            seg = seq[start:end]
            start += length
            end   += length

            # return segments until there aren't any left!
            if seg:
                yield seg
            else:
                raise StopIteration


    def _check_size_alignment (self, type, size):
        """
        Utility function to ensure that ``size`` is of the correct alignment for
        the data-type in ``type``.

        :param int type: one of the ``TYPE_BYTE``, ``TYPE_HALF``, or
                         ``TYPE_WORD`` constants
        :param int size: size (in bytes) of the data
        :raises:         ValueError

        """

        if type == scamp.TYPE_BYTE:
            pass
        elif type == scamp.TYPE_HALF:
            # must be aligned to a short boundary
            if size % 2:
                raise ValueError("data arranged as half-words but not aligned - size: %d" % size)
        elif type == scamp.TYPE_WORD:
            # must be aligned to a dword boundary
            if size % 4:
                raise ValueError("data arranged as words but not aligned - size: %d" % size)
        else:
            # incorrect data type
            raise ValueError("unknown data type: %d" % type)


    def write_mem_from_file(self, start_addr, type, filename,
                            chunk_size=16384):
        """
        Uploads the contents of a file to the target SpiNNaker node at a
        specific memory location.

        :param int start_addr: base address for the uploaded data
        :param int type:       one of ``TYPE_BYTE``, ``TYPE_HALF``, or
                               ``TYPE_WORD`` to indicate element type
        :param str filename:   name of the source file to read from
        :param int chunk_size: number of bytes to read from the file in one go
        :raises:               IOError, SCPError

        """

        # open the file and determine its length
        fd = file (filename, 'rb')
        fd.seek (0, os.SEEK_END)
        size = fd.tell ()
        fd.seek (0, os.SEEK_SET)

        # confirm the file is aligned correctly
        self._check_size_alignment (type, size)

        # read in the file in suitably sized chunks
        bytes_remaining = size
        addr            = start_addr
        while bytes_remaining > 0:
            # read a chunk and update the tracker variables
            chunk            = fd.read (chunk_size)
            bytes_remaining -= len (chunk)

            #print "Writing ",len(chunk)," bytes to ",hex(addr)," - ",bytes_remaining,"to go..."

            # write it into memory
            self.write_mem (addr, type, chunk)

            # update the address pointer
            addr += len (chunk)

        # close the file again
        fd.close ()

        return size

    def read_mem (self, start_addr, type, size):
        """
        Reads an amount of data from the target SpiNNaker node starting at
        address ``start_addr``.

        :param int start_addr: address to start reading from
        :param int type:       one of ``TYPE_BYTE``, ``TYPE_HALF``, or
                               ``TYPE_WORD`` to indicate element type
        :param int size:       number of bytes to read
        :returns:              string containing the data read
        :raises:               SCPError

        """

        msg = SCPMessage (cmd_rc=scamp.CMD_READ)

        # confirm the data size is aligned to the appropriate boundary
        self._check_size_alignment (type, size)

        # initialise tracker variables
        addr      = start_addr
        buf       = ''
        read_size = size

        # read all the data
        while (addr - start_addr) < size:
            # build up the packet as follows:
            #   arg1 = start address
            #   arg2 = chunk length
            #   arg3 = element size
            msg.arg1 = addr
            msg.arg2 = min (read_size, scamp.SDP_DATA_SIZE)
            msg.arg3 = type
            resp = self.transceiver.conn.send_scp_msg (msg)

            # add the data to the buffer and update the tracker variables
            buf       += resp.data
            addr      += len (resp.data)
            read_size -= len (resp.data)

        # return the (hopefully valid) data buffer
        return buf

    def read_mem_to_file (self, start_addr, type, size, filename,
                          chunk_size=16384):
        """
        Reads the memory of a target SpiNNaker node, starting from a specific
        location, and then writes it into a file.

        :param int start_addr: address to start reading from
        :param int type:       one of ``TYPE_BYTE``, ``TYPE_HALF``, or
                               ``TYPE_WORD`` to indicate element type
        :param str filename:   name of the destination file to write into
        :param int chunk_size: number of bytes to write to the file in one go
        :raises:               IOError, SCPError

        """

        # check the type alignment
        self._check_size_alignment (type, size)

        # open a file for writing
        fd = open (filename, 'wb')

        # iterate over the memory and write it into a file
        addr       = start_addr
        bytes_left = size
        while bytes_left > 0:
            # read a chunk from the SpiNNaker and update the counter variables
            chunk       = self.read_mem(addr, type,
                                        min(chunk_size, bytes_left))
            bytes_left -= len (chunk)
            addr       += len (chunk)

            # write it to the file
            fd.write (chunk)

        # close the file
        fd.close ()
