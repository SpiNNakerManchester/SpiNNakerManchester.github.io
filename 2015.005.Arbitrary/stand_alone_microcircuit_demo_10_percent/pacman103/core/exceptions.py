class SystemException(Exception):
    """
    Superclass of all exceptions from SpiNNaker hardware.
    """
    pass


class BoardDeadException(SystemException):
    """
    Thrown if a SpiNNaker board is uncontactable.
    """
    pass



class ProcessorDeadException(SystemException):
    """
    Thrown if a SpiNNaker processor is uncontactable.
    """
    pass



class PacmanException(Exception):
    """
    Superclass of all exceptions from PACMAN.
    """
    pass



class ExploreException(PacmanException):
    """
    Thrown if a SpiNNaker board is uncontactable, or not booted, or of insufficient dimensions
    """
    pass


class MissingParameterException(PacmanException):
    """
    Thrown if a model parameter required to build a data structure is missing.
    """
    pass



class PallocException(PacmanException):
    """
    Thrown if a processor allocation fails.
    """
    pass



class RallocException(PacmanException):
    """
    Thrown if a routing-table-entry allocation fails.
    """
    pass



class KallocException(PacmanException):
    """
    Thrown if a key-space allocation fails.
    """
    pass

class MissingSubclassMethodException(PacmanException):
    """
    Thrown if a subclass of a graph element is missing a
    method definition that should be present to override the 
    superclass method.
    """
    pass

class MissingSpecException(PacmanException):
    """
    Thrown if an expected Data Spec file is not found.
    """
    pass

class MalformedHeaderException(PacmanException):
    """
    Thrown if the format of the file header does not conform
    to expected structure, such as missing the required MAGIC
    NUMBER.
    """
    pass

class DsgFormatConversionError(PacmanException):
    """
    Thrown if the attempted re-scaling or reformating of a
    number fails due to being out of range or other wise malformed.
    """
    pass

class DsgSpecCmdException(PacmanException):
    """
    Thrown in the DSG or dsg_lib if a request to construct a 
    DataSpec command contained a malformed parameter (e.g. 
    out of range value).
    """
    pass

class DsgSpecMemAllocException(PacmanException):
    """
    Thrown in DSG if a memory request will exhaust the expected
    free SDRAM space on that target chip.
    """
    pass

class CantOpenForWriteException(PacmanException):
    """
    Thrown if an attempt to open a file for writing fails.
    """
    pass

class SpecExecMemAllocException(PacmanException):
    """
    Thrown in host-based Spec Executor if a memory request 
    will overwrite previously allocated memory on this chip.
    """
    pass

class SpecExecCmdException(PacmanException):
    """
    Thrown in the host-based Spec Executor if a DataSpec command
    contained a malformed parameter (e.g.  out of range value) or
    was grammatically incorrect (such as nested definitions,
    unexpected end of definition, etc.)
    """
    pass

class RouteTableDSGException(PacmanException):
    """
    Thrown in the route table generation phased (DSG) if an error
    has occured (e.g.) we have more than 1024 entries etc.
    """
    pass

class SpinnManException(PacmanException):
    '''
    thrown in the transceiver whenever an error has occured.
    '''
    pass

class VisuliserException(PacmanException):
    '''
    thrown from within the visuliser
    '''

class ConfigurationException(PacmanException):
    '''
    thrown from within the tool chain when a paramter passed from the user fails for any reason
    '''

class MemReadException(PacmanException):
    '''
    thrown from within the tool chain when asked to read a block of memory thats larger than what was allcoated for it
    '''

class RouterException(PacmanException):
    '''
    thrown from within the tool chain when an error occurs with the router object
    '''