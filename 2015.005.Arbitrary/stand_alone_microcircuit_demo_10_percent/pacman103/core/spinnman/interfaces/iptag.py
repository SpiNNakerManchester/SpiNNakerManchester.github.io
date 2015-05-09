__author__ = 'stokesa6'

class IPTag(object):
    #a class used for holding data that is contained within a IPTag

    def __init__(self, **kwargs):
        """
        Constructs an IPTag object.

        """
        members = ('ip', 'mac', 'port', 'timeout', 'flags',
                   'index', 'tag', 'hostname')

        # copy the given value or default to None
        for member in members:
            self.__dict__[member] = kwargs.setdefault (member, None)

    def __str__ (self):
        """
        Pretty print method to help in interactive mode.

        Print format:

            index: ip:port [mac]; flags, timeout

        """

        return '{:d}: {:s}:{:d} [{:s}]; {:x}, {:.02f}'.format (self.index,
            self.ip, self.port, self.mac, self.flags, self.timeout)

