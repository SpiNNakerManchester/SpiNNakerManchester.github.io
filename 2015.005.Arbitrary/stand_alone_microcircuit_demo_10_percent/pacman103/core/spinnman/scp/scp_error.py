# exceptions
import scamp

class SCPError (RuntimeError):
    """
    Error response from target SpiNNaker.

    :param int rc: response code from target SpiNNaker.
    :param msg: :py:class:`SCPMessage` that caused the error or ``None``

    """

    def __init__ (self, rc, msg=None):
        """
        Construct an :py:exc:`SCPError` object.

        """

        # get a nice custom error message
        super (SCPError, self).__init__ (
            "command failed with error %s: '%s'" % scamp.rc_to_string (rc))

        # save the response code
        self.rc      = rc
        self.rc_text = scamp.rc_to_string (rc)
        self.message = msg__author__ = 'stokesa6'
