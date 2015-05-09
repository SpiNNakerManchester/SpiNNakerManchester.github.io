
import logging
logger = logging.getLogger(__name__)

class EdgeConstraints:
    """
    Represents constraints on routing of an edge on a SpiNNaker board.

    **TODO**:
        decide upon implementation and usage.
    """

    def __init__(self):
        pass



class ExecutableTarget:
    """
    Represents a processor that should start an executable
    :param string fname: aplx filename
    :param int x: x-chip-coordinate.
    :param int y: y-chip-coordinate.
    :param int p: processor ID.
    """

    def __init__(self, fname, x, y, p):
        self.filename = fname
        self.targets = list()
        self.targets.append({'x': x, 'y': y, 'p': p})

    def __str__(self):
        output = ""
        for target in self.targets:
            output += "({},{},{}), ".format(target['x'], target['y'], target['p'])
        return "Executable target: {} '{}'".format(output, self.filename)

    def __repr__(self):
        return self.__str__()

    def printExecutableTarget(self):
        """
        Display the contents of one executable target object for debug purposes.
        """
        logger.debug(self.__str__())

class LoadTarget:
    """
    Represents a file that should be loaded into SpiNNaker before simulation.

    :param string fname: file to load.
    :param int x: x-chip-coordinate.
    :param int y: y-chip-coordinate.
    :param int p: processor ID.
    :param int a: target load address.
    """

    def __init__(self, fname, x, y, p, a):
        self.filename = fname
        self.x = x
        self.y = y
        self.p = p
        self.address = a

    def __str__(self):
        return "Load target: (%d, %d, %d), '%s' @ 0x%X" % \
            (self.x, self.y, self.p, self.filename, self.address)
    
    def __repr__(self):
        return self.__str__()
    
    def printLoadTarget(self):
        """
        Display the contents of one load target object for debug purposes.
        """
        logger.debug(self.__str__())



class MemWriteTarget:
    """
    Represents a 32-bit write to the memory of one chip that should occur before
    files are loaded.

    :param int x: x-chip-coordinate.
    :param int y: y-chip-coordinate.
    :param int p: processor ID.
    :param int a: address in memory for write
    :param int d: 32-bit data to be written (uint)
    """

    def __init__(self, x, y, p, a, d):
        self.x = x
        self.y = y
        self.p = p
        self.address = a
        self.data = d
    
    def __str__(self):
        return "Mem. target: (%d, %d, %d), 0x%X (%d) @ 0x%X" % \
            (self.x, self.y, self.p, self.data, self.data, self.address)
    
    def __repr__(self):
        return self.__str__()
    
    def printMemTarget(self):
        """
        Display the contents of one memory target object for debug purposes.
        """
        logger.debug(self.__str__())


class Placement:
    """
    Represents placement of a subvertex on a SpiNNaker processor.

    *Side effects*:
        Upon instantiation, the subvertex and the processor are updated to
        include a reference to the instance.

    :param `pacman103.lib.graph.Subvertex` subvertex: the placed subvertex.
    :param `pacman103.lib.lib_machine.Processor` subvertex:
        the allocated processor.
    """

    def __init__(self, subvertex, processor):
        # Store passed parameters
        self.subvertex = subvertex
        self.processor = processor
        # Set up references to self in subvertex and processor
        self.subvertex.placement = self



class Resources:
    """
    Represents the machine resources available to a processor or required by
    a subvertex.

    Division is overridden for this class, so that an object representing
    resource availability may be divided by one representing resource
    requirements, in order to find the number of atoms that can fit on one
    processor::

        requirements = vertex.model.get_requirements_per_atom()
        availability = machine.get_resources_per_processor()
        atoms_per_core = availability / requirements
    """

    def __init__(self, clock_ticks, dtcm, sdram):
        self.clock_ticks = clock_ticks
        self.dtcm = dtcm
        self.sdram = sdram
        
    def __str__(self):
        return ("Resources: clock_ticks=%d, dtcm=%d,"
               " sdram=%d" % (self.clock_ticks, self.dtcm, self.sdram))
    
    def __repr__(self):
        return self.__str__()


class Routing:
    """
    Represents the path of an edge over a SpiNNaker machine, as a list of
    `pacman103.lib.lib_map.RoutingEntry` objects.

    :param `pacman103.lib.graph.Subedge` subedge:
            parent subedge of the routing.
    """

    def __init__(self, subedge):
        self.subedge = subedge
        self.routing_entries = list()


    def add_entry(self, routing_entry):
        """
        Adds a routing entry to the routing.

        :param `pacman103.lib.lib_map.RoutingEntry` routing_entry:
            routing entry to add.
        """
        self.routing_entries.append(routing_entry)



class RoutingEntry(object):
    """
    Represents a routing entry in the memory of a SpiNNaker router.

    :param `pacman103.lib.lib_machine.Router` router:
        router to which this entry belongs
    :param int filename: routing filename (<= 2^32-1).
    :param int mask: routing mask (<= 2^32-1).
    """

    def __init__(self, router, filename, original_key, mask):
        # Store passed parameters
        self.router = router
        self.filename = filename
        self.original_key = original_key
        self.mask = mask
        # Set up route fields
        self.route = None
        self.defaultable = False
        # trace fields
        self.previous_router_entry = None
        self.previous_router_entry_direction = None
        self.next_router_entries = list()
        self.routing = None



class VertexConstraints:
    """
    Represents contraints on placement of a vertex on a SpiNNaker board.

    :param int x: x-coordinate of the chip on which the vertex must be placed.
    :param int y: y-coordinate of the chip on which the vertex must be placed.
    :param int p: processor on the chip where it must be placed (optional).
    """

    def __init__(self, x=None, y=None, p=None):
        self.x = x
        self.y = y
        self.p = p

    @property
    def placement_cardinality(self):
        return sum(x is not None for x in [self.x, self.y, self.p])

    def __str__(self):
        return "constraints:{},{},{},{}".format(self.x, self.y, self.p, self.placement_cardinality)














