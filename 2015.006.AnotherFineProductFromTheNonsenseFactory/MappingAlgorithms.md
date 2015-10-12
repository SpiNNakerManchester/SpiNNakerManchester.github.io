---
title: Adding new mapping algorithms to the SpiNNaker toolchain  
---

# Contents
* [Usage](#Usage)
* [Requirements](#Requirements)
* [Algorithm Metadata Xml File](#XMLMeta)
* [Json File Format](#Json)
* [Configuration](#Configuration)
* [Running Example](#RigPlacer)
* [Troubleshooting](#Trouble)

# <a name="Usage"></a> Usage of this functionality

The content of this page is to support end users whom wish to investigate the 
use of new mapping algorithms when intergrated into the SpiNNaker tool chain 
under 2015.006 (Another Fine Product From The Nonsense Factor).

This functionality allows algorithms coded in any langauge to be used in conjunction with the tool chain through the use of xml and json files.


# <a name="Requirements"></a> Requirements

To use this functionality, follow the instructions below:

1. git clone https://github.com/SpiNNakerManchester/sPyNNaker.git
1. cd sPyNNaker
1. git checkout mapping_work_flow
1. sudo python setup.py develop --no-deps
1. cd ..
1. git clone https://github.com/SpiNNakerManchester/PACMAN.git
1. cd PACMAN
1. git checkout mapping_work_flow
1. sudo python setup.py develop --no-deps
1. cd ..
1. git clone https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git
1. cd SpiNNFrontEndCommon
1. git checkout mapping_work_flow
1. sudo python setup.py develop --no-deps
1. cd ..
1. git clone https://github.com/SpiNNakerManchester/SpiNNakerGraphFrontEnd.git
1. cd SpiNNakerGraphFrontEnd
1. git checkout mapping_work_flow
1. sudo python setup.py develop --no-deps
1. cd ..
1. git clone https://github.com/SpiNNakerManchester/SpiNNMachine.git
1. cd SpiNNMachine
1. git checkout Mapping_Interface_changes
1. sudo python setup.py develop --no-deps
1. cd ..
1. git clone https://github.com/SpiNNakerManchester/SpiNNMan.git
1. cd SpiNNMan
1. git checkout Mapping_Interface_changes
1. sudo python setup.py develop --no-deps
1. cd ..
1. git clone https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin.git
1. cd sPyNNakerExternalDevicesPlugin
1. git checkout Mapping_Interface_changes
1. sudo python setup.py develop --no-deps
1. cd ..

This now gives you a updated version of the tool chain, which supports new 
mapping algorithms. It is worth noting that when 2015.006 
(Another Fine Product From The Nonsense Factor) is offically released, 
these installation instructions will be no longer required.

# <a name="XMLMeta"></a> Algorithm Metadata Xml File

As end users can add any arbitary number of algorithms to the PACMAN flow, 
this means there is no longer a predefined logic flow between algorithms. 
To rectify this, there is a block of code located in https://github.com/SpiNNakerManchester/PACMAN/blob/mapping_work_flow/pacman/operations/pacman_algorithm_executor.py which takes a description of the inputs, outputs, and executable paramters of the algorithms which it has been instructed to use and deduces the logical order of algorithms.

Any new algorithm needs to have a XMl file which states how to execute the algorithm, its inputs and outputs. Below is an example xml file:

```
<algorithms>
    <algorithm name="BasicPartitioner">
        <python_module>pacman.operations.partition_algorithms.basic_partitioner</python_module>
        <python_class>BasicPartitioner</python_class>
        <required_inputs>
            <parameter>
                <param_name>graph</param_name>
                <param_type>MemoryPartitionableGraph</param_type>
            </parameter>
            <parameter>
                <param_name>machine</param_name>
                <param_type>MemoryExtendedMachine</param_type>
            </parameter>
        </required_inputs>
        <produces_outputs>
            <parameter>
                <param_name>Partitioned_graph</param_name>
                <param_type>MemoryPartitionedGraph</param_type>
            </parameter>
            <parameter>
                <param_name>Graph_mapper</param_name>
                <param_type>MemoryGraphMapper</param_type>
            </parameter>
        </produces_outputs>
    </algorithm>
    <algorithm name="RigCommandLineSAPlacer">
        <command_line_args>
            <arg>python</arg>
            <arg>rig_place.py</arg>
            <arg>--algorithm=sa</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements_path}</arg>
        </command_line_args>
        <required_inputs>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FilePartitionedGraph</param_type>
            </parameter>
            <parameter>
                <param_name>machine</param_name>
                <param_type>FileMachine</param_type>
            </parameter>
            <parameter>
                <param_name>constraints</param_name>
                <param_type>FileConstraints</param_type>
            </parameter>
            <parameter>
                <param_name>placements_path</param_name>
                <param_type>FilePlacementFilePath</param_type>
            </parameter>
        </required_inputs>
        <produces_outputs>
            <parameter>
                <param_name>FilePlacementFilePath</param_name>
                <param_type>FilePlacements</param_type>
            </parameter>
        </produces_outputs>
    </algorithm>
</algorithms>
```

This example xml shows 2 algorithms descriptions (the BasicPartitioner which is an internal algorithm for PACMAN and an external placing algorithm known as RigCommandLineSAPlacer) All algorithms defined in this file must reside between the <algorithms> tag, and each algorthm needs to be encapsulated between <algorithm> tags. Each Algorithm has a name (referred to by the <algorithm name=> tag) which is used during configuration to identify what algorithums to run. Below is a breakdown of how this xml file describes the two algorithms.

The BasicPartitioner takes 2 parameters as its inputs, which are defined by the parameters encapsulated within the <required_inputs>, <param_name> and <param_type> tags. These are:

1. The partitionable graph which has a type of MemoryPartitionableGraph for clarity,
1. and a python represnetation of the SpiNNaker machine which has been extended to represent external devices as virtual chips, which has a type of MemoryExtendedMachine for clarity.
 
The BasicPartitioner generates 2 outputs, which are defined by the parameters encapulated within the <produces_outputs>, <param_name> and <param_type> tags. These are:

1. The partitioned graph where each vertex is a core sized chunk of a  vertex in the partitionable graph which has a type of MemoryPartitionedGraph for clarity, 
1. and a mapping between the partitionable and partitioned graph, known as a graph mapper whcih has a type of MemorygraphMapper for clarity. 
 
Because the BasicPartitioner is a internal algorthm of PACMAN and therefore uses the PACMAN data structures, it can be ran directly as a imported python module. Therefore the tool chain needs to know where the module lives (in relation to the PACMAN insall) and what class to instansiate and call. These pieces of data can be found in the <python_module> and <python_class> tags. 

The RigCommandLineSAPlacer on the otherhand is a external algorthim to PACMAN and therefore has to be ran as a command runnable from the command line. The RigCommandLineSAPlacer takes 5 parameters as its command line inputs, and requires 2 commands to run. These are encapsulated within the <command_line_args> and <arg> tags. These arguments are as follows:

The first and second arguments state that its a python class to run, and the path requried to make the script run from the command line. Here we have assumed that the script can be ran direclty from anywhere. The rest of the arguments corraspond to inputs to the algorithm and are tied to the <required_inputs> tags. These are described below:

1. The algorithm to use. This algorithm is a interface for a collection of placers and because the tool chain can only process each algorithm individually, this means in this case, that it is hard coded and therefore is not needed in the <required_inputs> tags.
1. A file representation of the PACMAN's partitioned_graph is required under the parameter --graph. This is deduced from the required input which has the parameter_name of graph and type of FilePartitionedGraph.  
1. A file representation of the SpiNNaker machine is required under the parameter --machine. This is deduced from the required input which has the parameter_name of machine and type FileMachine. 
1. A file that contains contraints on vertices within the partitioned graph is required under the parameter --constraints. This is deduced from the required input which has the parameter_name of constraints and type FileConstraints. 
1. A filepath for where to write the output json file for its FilePlacements is required under the parameter --placements. This is deduced from the required input which has the name placements_path and has the type FilePlacementFilePath.

The RigCommandLineSAPlacer also produces one output, which is the json file which conatains placement infoformation. This is deduced from the <produces_outputs> tags. Note that the param_name is the same as the input type for the placements_path. This allows the PACMAN algorithm to deduce what type of data your outputting, whilst supporting general naming of output files. 

The tool chain currently supplies a collection of inputs into the PACMAN infranstrucutre. These are defined below and can be found from lines 194 to 206 of [spinnaker.py](https://github.com/SpiNNakerManchester/sPyNNaker/blob/mapping_work_flow/spynnaker/pyNN/spinnaker.py):

|Name|Definition|
|-----------------|------------------|
|MemoryPartitionableGraph|python object for the partitionable graph|
|MemoryMachine|python object of the spiNNaker machine|
|ReportFolder|the filepath for where to write reports|
|IPAddress|the ipaddress for the SpiNNaker machine|
|Transciever| the python interface to the SpiNNaker machine|
|FileCoreAllocationsFilePath|the filepath for writing core allocations|
|FileSDRAMAllocationsFilePath|the filepath for writing sdram allocations|
|FileMachineFilePath|the filepath for writing the json represnetation of the SpiNNaker machine produced by PACMAN|
|FilePartitionedGraphFilePath|the filepath for writing the json represnetation of the partitioned graph produced by PACMAN| 
|FilePlacementFilePath|the filepath for writing the json representation of the placements produced by PACMAN|
|FileRouingPathsFilePath|the filepath for writing the json represnetation of the routing paths|
|FileConstraintsFilePath|the filepath for writing the json represnetation of the constraints from the partitioned graph|

The tool chain also provides a collection of converters which switch between json file formats and PACMANS data objects. These can be found in the (pacman/utilities/file_format_converters)[https://github.com/SpiNNakerManchester/PACMAN/blob/mapping_work_flow/pacman/utilities/file_format_converters]. The XML file describing their inputs and outputs can be found in the same folder under (converter_algorithms_metadata.xml)[https://github.com/SpiNNakerManchester/PACMAN/blob/mapping_work_flow/pacman/utilities/file_format_converters/converter_algorithms_metadata.xml]. These are summerised below:

|Name|Definition|Inputs|Outputs|Currently Implimented?|
|-----------------|------------------|-------------|-------------|--------|
|ConvertToFilePlacement|Converts from PACMAN placements to Json Placements| MemoryPlacements, FilePlacementFilePath| FilePlacements| True|
|ConvertToFilePartitionedGraph|Converts from PACMAN partitioned graph to Json partitioned graph| MemoryPartitionedGraph, FilePartitionedGraphFilePath| FilePartitionedGraph| True|
|ConvertToFileCoreAllocation|Converts PACMAN placements to the Json core_allocations| MemoryPlacements, FileCoreAllocationsFilePath| FileCoreAllocations| True|
|ConvertToFileMachine|Converts from the PACMAN machine object to the Json Machine| MemoryMachine, FileMachineFilePath|FileMachine| True|
|CreateToFileConstraints|Creates the Json constraints file from PACMAN machien with virutal chips and the PACMAN partitioned graph| MemoryExtendedMachine, MemoryPartitionedGraph, FileConstraintsFilePath| FileConstraints| True|
|ConvertToFilePartitionableGraph|Converts from PACMAN partitionable graph to Json partitionable graph| MemoryPartitionableGraph, FilePartitionableGraphFilePath|FilePartitionableGraph| False|
|ConvertToFileRoutingTables|Converts PACMAN routing tables into Json routing tables| MemoryRoutingTables, FileRoutingTablesFilePath|FileRoutingTables| False|
|ConvertToMemoryPlacements|Converts from the Json placement, core_allocation to the PACMAN placements, which requires PACMANS partitioned graph| MemoryExtendedMachine, FilePlacements, MemoryPartitionedGraph, FileCoreAllocations, FileConstraints| MemoryPlacements| True|
|ConvertToMemoryMultiCastRoutingPaths|Converts Json routing_paths to PACMAN routing paths with the use of PACMAN's partitioned graph, placements, and machine with virutal chips| FileRoutingPaths, MemoryPartitionedGraph, MemoryPlacements, MemoryExtendedMachine| MemoryRoutingPaths| True|
|ConvertToMemoryRoutingTables|Converts Json routing tables into PACMAN routing tables| FileRoutingtables|MemoryRoutingTables|False|
|ConvertToMemoryPartitionedGraph|Converts Json partitioned graph into PACMAN partitioned graph| FilePartitionedGraph|MemoryPartitionedGraph| False|

The tool chain expects to be able to extract a umber of PACMAN objects at the end of the algortihm exeuction. This is aminly for transmitting the objects onto the SpiNNaker machine, and supporting data retrival lateron. These objects are as follows:

|Name|Definition|
|-----------------|------------------|
|MemoryPlacements| The PACMAN representation of the placements. |
|MemoryRoutingTables| The PACMAN represnetation of the entries used on each routing table.|
|MemoryRoutingInfos| The PACMAN representation of the keys and masks allocated to each edge in the partitioned graph.|
|MemoryTags| The PACMAN reprensetation of the tags allocated to the subvertices of the partitioned graph.|
|MemoryPartitionedGraph| The PACMAN represnetation of the partitioned graph.|
|MemoryGraphMapper| The PACMAN represnetation of the mapping between partitionable and partitioned graphs.|


# <a name="Json"></a> Json File Format

we refer you to the documentation on the Json File Format found (here)[https://github.com/mossblaser/place-and-route-interchange-format]

# <a name="Configuration"></a> Configuration

To configure the sPyNNaker front end to use your algorithms, you must first have the xml file mentioned in [Algorithm Metadata Xml File](#XMLMeta) for your algorithm and have added the Json converters to your algorthim's front end. Then you will need to open your .spynnaker.cfg file and add these extra regions and params.

```
[Mapping]
# format is <algorithum_name>,<>
# pacman algorithms are:
# Basic_dijkstra_routing, RadialPlacer, BasicPlacer, ConnectiveBasedPlacer,
# BasicTagAllocator, BasicPartitioner, PartitionAndPlacePartitioner,
# BasicRoutingInfoAllocator, BasicDijkstraRouting,
# MallocBasedRoutingInfoAllocator, GraphEdgeFilter, EdgeToNKeysMapper
algorithms = MallocBasedChipIDAllocator,BasicDijkstraRouting,RadialPlacer,BasicTagAllocator,PartitionAndPlacePartitioner,MallocBasedRoutingInfoAllocator,GraphEdgeFilter,EdgeToNKeysMapper
# format is <path1>,<path2>
extra_xmls_paths = None
```

At this point, you need to :
1. Remove the PACMAN specific algorithm that you'r algorithm replaces.
1. Add your algorithms name (as specified in the <algorithm name=""> tag) to the list.
1. add a path to your XML file containing its input and output data in the "extra_xml_paths"
1. run a pynn script.

# <a name="RigPlacer"></a> Running Example

To run a simple example of using external and internal algorithms in situ, please follow these instructions:
1. install rig (this can be done via the command pip install rig)
1. git clone https://github.com/mossblaser/place-and-route-interchange-format.git
1. create a xml file with the following data:

```
<algorithms>
    <algorithm name="RigCommandLineSAPlacer">
        <command_line_args>
            <arg>python</arg>
            <arg>PATH_TO_GIT_CLONE/rig_place.py</arg>
            <arg>--algorithm=sa</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements_path}</arg>

        </command_line_args>
         <required_inputs>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FilePartitionedGraph</param_type>
            </parameter>
            <parameter>
                <param_name>machine</param_name>
                <param_type>FileMachine</param_type>
            </parameter>
            <parameter>
                <param_name>constraints</param_name>
                <param_type>FileConstraints</param_type>
            </parameter>
             <parameter>
                <param_name>placements_path</param_name>
                <param_type>FilePlacementFilePath</param_type>
            </parameter>
        </required_inputs>
        <parameters>
        </parameters>
        <produces_outputs>
            <parameter>
                <param_name>FilePlacementFilePath</param_name>
                <param_type>FilePlacements</param_type>
            </parameter>
        </produces_outputs>
    </algorithm>
    <algorithm name="RigCommandLineHilbertPlacer">
        <command_line_args>
            <arg>python</arg>
            <arg>PATH_TO_GIT_CLONE/rig_place.py</arg>
            <arg>--algorithm=hilbert</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements_path}</arg>

        </command_line_args>
         <required_inputs>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FilePartitionedGraph</param_type>
            </parameter>
            <parameter>
                <param_name>machine</param_name>
                <param_type>FileMachine</param_type>
            </parameter>
            <parameter>
                <param_name>constraints</param_name>
                <param_type>FileConstraints</param_type>
            </parameter>
             <parameter>
                <param_name>placements_path</param_name>
                <param_type>FilePlacementFilePath</param_type>
            </parameter>
        </required_inputs>
        <parameters>
        </parameters>
        <produces_outputs>
            <parameter>
                <param_name>FilePlacementFilePath</param_name>
                <param_type>FilePlacements</param_type>
            </parameter>
        </produces_outputs>
    </algorithm>
    <algorithm name="RigAllocator">
        <command_line_args>
            <arg>python</arg>
            <arg>PATH_TO_GIT_CLONE/rig_allocate.py</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements}</arg>
            <arg>--algorithm=greedy</arg>
            <arg>--allocations=cores:{core_allocation_path}</arg>
            <arg>--allocations=sdram:{sdram_allocation_path}</arg>
        </command_line_args>
         <required_inputs>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FilePartitionedGraph</param_type>
            </parameter>
            <parameter>
                <param_name>machine</param_name>
                <param_type>FileMachine</param_type>
            </parameter>
            <parameter>
                <param_name>constraints</param_name>
                <param_type>FileConstraints</param_type>
            </parameter>
            <parameter>
                <param_name>placements</param_name>
                <param_type>FilePlacements</param_type>
            </parameter>
            <parameter>
                <param_name>core_allocation_path</param_name>
                <param_type>FileCoreAllocationsFilePath</param_type>
            </parameter>
             <parameter>
                <param_name>sdram_allocation_path</param_name>
                <param_type>FileSDRAMAllocationsFilePath</param_type>
            </parameter>
        </required_inputs>
        <parameters>
        </parameters>
        <produces_outputs>
            <parameter>
                <param_name>FileCoreAllocationsFilePath</param_name>
                <param_type>FileCoreAllocations</param_type>
            </parameter>
        </produces_outputs>
    </algorithm>
    <algorithm name="RigRouter">
        <command_line_args>
            <arg>python</arg>
            <arg>PATH_TO_GIT_CLONE/rig_route.py</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements}</arg>
            <arg>--allocations=cores:{allocations}</arg>
            <arg>--algorithm=ner</arg>
            <arg>--core-resource=cores</arg>
            <arg>--routes={routing_paths_file_path}</arg>
        </command_line_args>
         <required_inputs>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FilePartitionedGraph</param_type>
            </parameter>
            <parameter>
                <param_name>machine</param_name>
                <param_type>FileMachine</param_type>
            </parameter>
            <parameter>
                <param_name>constraints</param_name>
                <param_type>FileConstraints</param_type>
            </parameter>
            <parameter>
                <param_name>placements</param_name>
                <param_type>FilePlacements</param_type>
            </parameter>
            <parameter>
                <param_name>allocations</param_name>
                <param_type>FileCoreAllocations</param_type>
            </parameter>
             <parameter>
                <param_name>routing_paths_file_path</param_name>
                <param_type>FileRouingPathsFilePath</param_type>
            </parameter>
        </required_inputs>
        <parameters>
        </parameters>
        <produces_outputs>
            <parameter>
                <param_name>FileRouingPathsFilePath</param_name>
                <param_type>FileRoutingPaths</param_type>
            </parameter>
        </produces_outputs>
    </algorithm>
</algorithms>
```

1. Replace PATH_TO_GIT_CLONE in the xml file with the absolute path to the git clone from before.
1. modify your .spynnaker.cfg file to include the following lines:

```
[Mapping]

# format is  <algorithum_name>,<>
# pacman algorithms are:
# Basic_dijkstra_routing, RadialPlacer, BasicPlacer, ConnectiveBasedPlacer,
# BasicTagAllocator, BasicPartitioner, PartitionAndPlacePartitioner,
# BasicRoutingInfoAllocator, BasicDijkstraRouting,
# MallocBasedRoutingInfoAllocator, GraphEdgeFilter, EdgeToNKeysMapper
algorithms = MallocBasedChipIDAllocator,RigRouter,RigCommandLineHilbertPlacer,RigAllocator,BasicTagAllocator,PartitionAndPlacePartitioner,MallocBasedRoutingInfoAllocator,GraphEdgeFilter,EdgeToNKeysMapper
# format is <path1>,<path2>
extra_xmls_paths = PATH_TO_XML_FILE

```

1. replace PATH_TO_XML_FILE with a absolute path to the xml file you just wrote.
1.  (PyNNExamples)[https://github.com/SpiNNakerManchester/PyNNExamples]
1. run python PyNNExamples/examples/synfire_if_curr_exp.py

You should see output like the one below:

```
/usr/bin/python2.7 /home/S06/stokesa6/spinniker/alpha_package_103_git/PyNNExamples/examples/synfire_if_curr_exp.py
2015-10-12 12:02:13 INFO: Read config files: /home/S06/stokesa6/.spynnaker.cfg, /home/S06/stokesa6/spinniker/alpha_package_103_git/sPyNNaker/spynnaker/spynnaker.cfg, /home/S06/stokesa6/spinniker/alpha_package_103_git/spinn-6_boards_from_base.cfg
2015-10-12 12:02:14 INFO: sPyNNaker (c) 2015 APT Group, University of Manchester
2015-10-12 12:02:14 INFO: Release version 2015.005(Arbitrary) - September 2015. Installed in folder /home/S06/stokesa6/spinniker/alpha_package_103_git/sPyNNaker
2015-10-12 12:02:14 INFO: Setting time scale factor to 1.
2015-10-12 12:02:14 INFO: Setting appID to 30.
2015-10-12 12:02:14 INFO: Setting machine time step to 1000.0 micro-seconds.
2015-10-12 12:02:14 WARNING: You are trying to record the conductance from a model which does not contain conductance behaviour. You will recieve current measurements instead. Sorry
2015-10-12 12:02:14 INFO: Creating transceiver for cspc276
2015-10-12 12:02:14 INFO: going to try to boot the machine with scamp
2015-10-12 12:02:14 INFO: Detected a machine on ip address 130.88.198.208 which has 5138 cores and 864 links
2015-10-12 12:02:14 INFO: successfully booted the machine with scamp
2015-10-12 12:02:15 INFO: *** Running Mapper *** 
Allocating virtual identifiers
|0                           50%                         100%|
 ============================================================
Partitioning graph vertices
|0                           50%                         100%|
 ============================================================
on partitioning the partitionable_graph's edges
|0                           50%                         100%|
 ============================================================
Filtering edges
|0                           50%                         100%|
 ============================================================
creating json constraints
|0                           50%                         100%|
 ============================================================
Converting to json machine
|0                           50%                         100%|
 ============================================================
Converting to json partitioned graph
|0                           50%                         100%|
 ============================================================
Running external algorithm RigCommandLineHilbertPlacer
|0                           50%                         100%|
 ============================================================
Running external algorithm RigAllocator
|0                           50%                         100%|
 ============================================================
Running external algorithm RigRouter
|0                           50%                         100%|
 ============================================================
Allocating tags
|0                           50%                         100%|
 ============================================================
Converting to PACMAN routing paths
|0                           50%                         100%|
 ============================================================
Allocating routing keys
|0                           50%                         100%|
 ============================================================
Verifying the routes from each core travel to the correct locations
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:16 INFO: Time to map model: 0:00:00.791293
2015-10-12 12:02:16 INFO: *** Generating Output *** 
Generating data specifications
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:16 INFO: Time to generate data: 0:00:00.215988
Executing data specifications
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:16 INFO: Time to execute data specifications: 0:00:00.055907
2015-10-12 12:02:16 INFO: *** Loading tags ***
2015-10-12 12:02:16 INFO: *** Loading data ***
Loading application data onto the machine
|0                           50%                         100%|
 ============================================================
Loading routing data onto the machine
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:16 INFO: *** Loading executables ***
Loading executables onto the machine
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:18 INFO: *** Loading buffers ***
Initialising buffers
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:18 INFO: *** Running simulation... *** 
Loading buffers (12 bytes)
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:18 INFO: Starting application
2015-10-12 12:02:18 INFO: Checking that the application has started
2015-10-12 12:02:18 INFO: Application started - waiting 6.0 seconds for it to stop
2015-10-12 12:02:24 INFO: Application has run to completion
Getting provenance data
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:25 INFO: Getting v for pop_1
Getting recorded v for pop_1
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:34 INFO: Time to read v: 0:00:08.764159
2015-10-12 12:02:34 INFO: Getting gsyn for pop_1
Getting recorded gsyn for pop_1
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:49 INFO: Time to get gsyn: 0:00:14.429882
Getting spikes for pop_1
|0                           50%                         100%|
 ============================================================
2015-10-12 12:02:49 INFO: Time to get spikes: 0:00:00.674058
[[  0.00000000e+00   3.00000000e+00]
 [  0.00000000e+00   3.80300000e+03]
 [  1.00000000e+00   2.20000000e+01]
 [  1.00000000e+00   3.82200000e+03]
 [  2.00000000e+00   4.10000000e+01]
 [  2.00000000e+00   3.84100000e+03]
 [  3.00000000e+00   6.00000000e+01]
 [  3.00000000e+00   3.86000000e+03]
 [  4.00000000e+00   7.90000000e+01]
 [  4.00000000e+00   3.87900000e+03]
 [  5.00000000e+00   9.80000000e+01]
 [  5.00000000e+00   3.89800000e+03]
 [  6.00000000e+00   1.17000000e+02]
 [  6.00000000e+00   3.91700000e+03]
 [  7.00000000e+00   1.36000000e+02]
 [  7.00000000e+00   3.93600000e+03]
 [  8.00000000e+00   1.55000000e+02]
 [  8.00000000e+00   3.95500000e+03]
 [  9.00000000e+00   1.74000000e+02]
 [  9.00000000e+00   3.97400000e+03]
 [  1.00000000e+01   1.93000000e+02]
 [  1.00000000e+01   3.99300000e+03]
 [  1.10000000e+01   2.12000000e+02]
 [  1.10000000e+01   4.01200000e+03]
 [  1.20000000e+01   2.31000000e+02]
 [  1.20000000e+01   4.03100000e+03]
 [  1.30000000e+01   2.50000000e+02]
 [  1.30000000e+01   4.05000000e+03]
 [  1.40000000e+01   2.69000000e+02]
 [  1.40000000e+01   4.06900000e+03]
 [  1.50000000e+01   2.88000000e+02]
 [  1.50000000e+01   4.08800000e+03]
 [  1.60000000e+01   3.07000000e+02]
 [  1.60000000e+01   4.10700000e+03]
 [  1.70000000e+01   3.26000000e+02]
 [  1.70000000e+01   4.12600000e+03]
 [  1.80000000e+01   3.45000000e+02]
 [  1.80000000e+01   4.14500000e+03]
 [  1.90000000e+01   3.64000000e+02]
 [  1.90000000e+01   4.16400000e+03]
 [  2.00000000e+01   3.83000000e+02]
 [  2.00000000e+01   4.18300000e+03]
 [  2.10000000e+01   4.02000000e+02]
 [  2.10000000e+01   4.20200000e+03]
 [  2.20000000e+01   4.21000000e+02]
 [  2.20000000e+01   4.22100000e+03]
 [  2.30000000e+01   4.40000000e+02]
 [  2.30000000e+01   4.24000000e+03]
 [  2.40000000e+01   4.59000000e+02]
 [  2.40000000e+01   4.25900000e+03]
 [  2.50000000e+01   4.78000000e+02]
 [  2.50000000e+01   4.27800000e+03]
 [  2.60000000e+01   4.97000000e+02]
 [  2.60000000e+01   4.29700000e+03]
 [  2.70000000e+01   5.16000000e+02]
 [  2.70000000e+01   4.31600000e+03]
 [  2.80000000e+01   5.35000000e+02]
 [  2.80000000e+01   4.33500000e+03]
 [  2.90000000e+01   5.54000000e+02]
 [  2.90000000e+01   4.35400000e+03]
 [  3.00000000e+01   5.73000000e+02]
 [  3.00000000e+01   4.37300000e+03]
 [  3.10000000e+01   5.92000000e+02]
 [  3.10000000e+01   4.39200000e+03]
 [  3.20000000e+01   6.11000000e+02]
 [  3.20000000e+01   4.41100000e+03]
 [  3.30000000e+01   6.30000000e+02]
 [  3.30000000e+01   4.43000000e+03]
 [  3.40000000e+01   6.49000000e+02]
 [  3.40000000e+01   4.44900000e+03]
 [  3.50000000e+01   6.68000000e+02]
 [  3.50000000e+01   4.46800000e+03]
 [  3.60000000e+01   6.87000000e+02]
 [  3.60000000e+01   4.48700000e+03]
 [  3.70000000e+01   7.06000000e+02]
 [  3.70000000e+01   4.50600000e+03]
 [  3.80000000e+01   7.25000000e+02]
 [  3.80000000e+01   4.52500000e+03]
 [  3.90000000e+01   7.44000000e+02]
 [  3.90000000e+01   4.54400000e+03]
 [  4.00000000e+01   7.63000000e+02]
 [  4.00000000e+01   4.56300000e+03]
 [  4.10000000e+01   7.82000000e+02]
 [  4.10000000e+01   4.58200000e+03]
 [  4.20000000e+01   8.01000000e+02]
 [  4.20000000e+01   4.60100000e+03]
 [  4.30000000e+01   8.20000000e+02]
 [  4.30000000e+01   4.62000000e+03]
 [  4.40000000e+01   8.39000000e+02]
 [  4.40000000e+01   4.63900000e+03]
 [  4.50000000e+01   8.58000000e+02]
 [  4.50000000e+01   4.65800000e+03]
 [  4.60000000e+01   8.77000000e+02]
 [  4.60000000e+01   4.67700000e+03]
 [  4.70000000e+01   8.96000000e+02]
 [  4.70000000e+01   4.69600000e+03]
 [  4.80000000e+01   9.15000000e+02]
 [  4.80000000e+01   4.71500000e+03]
 [  4.90000000e+01   9.34000000e+02]
 [  4.90000000e+01   4.73400000e+03]
 [  5.00000000e+01   9.53000000e+02]
 [  5.00000000e+01   4.75300000e+03]
 [  5.10000000e+01   9.72000000e+02]
 [  5.10000000e+01   4.77200000e+03]
 [  5.20000000e+01   9.91000000e+02]
 [  5.20000000e+01   4.79100000e+03]
 [  5.30000000e+01   1.01000000e+03]
 [  5.30000000e+01   4.81000000e+03]
 [  5.40000000e+01   1.02900000e+03]
 [  5.40000000e+01   4.82900000e+03]
 [  5.50000000e+01   1.04800000e+03]
 [  5.50000000e+01   4.84800000e+03]
 [  5.60000000e+01   1.06700000e+03]
 [  5.60000000e+01   4.86700000e+03]
 [  5.70000000e+01   1.08600000e+03]
 [  5.70000000e+01   4.88600000e+03]
 [  5.80000000e+01   1.10500000e+03]
 [  5.80000000e+01   4.90500000e+03]
 [  5.90000000e+01   1.12400000e+03]
 [  5.90000000e+01   4.92400000e+03]
 [  6.00000000e+01   1.14300000e+03]
 [  6.00000000e+01   4.94300000e+03]
 [  6.10000000e+01   1.16200000e+03]
 [  6.10000000e+01   4.96200000e+03]
 [  6.20000000e+01   1.18100000e+03]
 [  6.20000000e+01   4.98100000e+03]
 [  6.30000000e+01   1.20000000e+03]
 [  6.40000000e+01   1.21900000e+03]
 [  6.50000000e+01   1.23800000e+03]
 [  6.60000000e+01   1.25700000e+03]
 [  6.70000000e+01   1.27600000e+03]
 [  6.80000000e+01   1.29500000e+03]
 [  6.90000000e+01   1.31400000e+03]
 [  7.00000000e+01   1.33300000e+03]
 [  7.10000000e+01   1.35200000e+03]
 [  7.20000000e+01   1.37100000e+03]
 [  7.30000000e+01   1.39000000e+03]
 [  7.40000000e+01   1.40900000e+03]
 [  7.50000000e+01   1.42800000e+03]
 [  7.60000000e+01   1.44700000e+03]
 [  7.70000000e+01   1.46600000e+03]
 [  7.80000000e+01   1.48500000e+03]
 [  7.90000000e+01   1.50400000e+03]
 [  8.00000000e+01   1.52300000e+03]
 [  8.10000000e+01   1.54200000e+03]
 [  8.20000000e+01   1.56100000e+03]
 [  8.30000000e+01   1.58000000e+03]
 [  8.40000000e+01   1.59900000e+03]
 [  8.50000000e+01   1.61800000e+03]
 [  8.60000000e+01   1.63700000e+03]
 [  8.70000000e+01   1.65600000e+03]
 [  8.80000000e+01   1.67500000e+03]
 [  8.90000000e+01   1.69400000e+03]
 [  9.00000000e+01   1.71300000e+03]
 [  9.10000000e+01   1.73200000e+03]
 [  9.20000000e+01   1.75100000e+03]
 [  9.30000000e+01   1.77000000e+03]
 [  9.40000000e+01   1.78900000e+03]
 [  9.50000000e+01   1.80800000e+03]
 [  9.60000000e+01   1.82700000e+03]
 [  9.70000000e+01   1.84600000e+03]
 [  9.80000000e+01   1.86500000e+03]
 [  9.90000000e+01   1.88400000e+03]
 [  1.00000000e+02   1.90300000e+03]
 [  1.01000000e+02   1.92200000e+03]
 [  1.02000000e+02   1.94100000e+03]
 [  1.03000000e+02   1.96000000e+03]
 [  1.04000000e+02   1.97900000e+03]
 [  1.05000000e+02   1.99800000e+03]
 [  1.06000000e+02   2.01700000e+03]
 [  1.07000000e+02   2.03600000e+03]
 [  1.08000000e+02   2.05500000e+03]
 [  1.09000000e+02   2.07400000e+03]
 [  1.10000000e+02   2.09300000e+03]
 [  1.11000000e+02   2.11200000e+03]
 [  1.12000000e+02   2.13100000e+03]
 [  1.13000000e+02   2.15000000e+03]
 [  1.14000000e+02   2.16900000e+03]
 [  1.15000000e+02   2.18800000e+03]
 [  1.16000000e+02   2.20700000e+03]
 [  1.17000000e+02   2.22600000e+03]
 [  1.18000000e+02   2.24500000e+03]
 [  1.19000000e+02   2.26400000e+03]
 [  1.20000000e+02   2.28300000e+03]
 [  1.21000000e+02   2.30200000e+03]
 [  1.22000000e+02   2.32100000e+03]
 [  1.23000000e+02   2.34000000e+03]
 [  1.24000000e+02   2.35900000e+03]
 [  1.25000000e+02   2.37800000e+03]
 [  1.26000000e+02   2.39700000e+03]
 [  1.27000000e+02   2.41600000e+03]
 [  1.28000000e+02   2.43500000e+03]
 [  1.29000000e+02   2.45400000e+03]
 [  1.30000000e+02   2.47300000e+03]
 [  1.31000000e+02   2.49200000e+03]
 [  1.32000000e+02   2.51100000e+03]
 [  1.33000000e+02   2.53000000e+03]
 [  1.34000000e+02   2.54900000e+03]
 [  1.35000000e+02   2.56800000e+03]
 [  1.36000000e+02   2.58700000e+03]
 [  1.37000000e+02   2.60600000e+03]
 [  1.38000000e+02   2.62500000e+03]
 [  1.39000000e+02   2.64400000e+03]
 [  1.40000000e+02   2.66300000e+03]
 [  1.41000000e+02   2.68200000e+03]
 [  1.42000000e+02   2.70100000e+03]
 [  1.43000000e+02   2.72000000e+03]
 [  1.44000000e+02   2.73900000e+03]
 [  1.45000000e+02   2.75800000e+03]
 [  1.46000000e+02   2.77700000e+03]
 [  1.47000000e+02   2.79600000e+03]
 [  1.48000000e+02   2.81500000e+03]
 [  1.49000000e+02   2.83400000e+03]
 [  1.50000000e+02   2.85300000e+03]
 [  1.51000000e+02   2.87200000e+03]
 [  1.52000000e+02   2.89100000e+03]
 [  1.53000000e+02   2.91000000e+03]
 [  1.54000000e+02   2.92900000e+03]
 [  1.55000000e+02   2.94800000e+03]
 [  1.56000000e+02   2.96700000e+03]
 [  1.57000000e+02   2.98600000e+03]
 [  1.58000000e+02   3.00500000e+03]
 [  1.59000000e+02   3.02400000e+03]
 [  1.60000000e+02   3.04300000e+03]
 [  1.61000000e+02   3.06200000e+03]
 [  1.62000000e+02   3.08100000e+03]
 [  1.63000000e+02   3.10000000e+03]
 [  1.64000000e+02   3.11900000e+03]
 [  1.65000000e+02   3.13800000e+03]
 [  1.66000000e+02   3.15700000e+03]
 [  1.67000000e+02   3.17600000e+03]
 [  1.68000000e+02   3.19500000e+03]
 [  1.69000000e+02   3.21400000e+03]
 [  1.70000000e+02   3.23300000e+03]
 [  1.71000000e+02   3.25200000e+03]
 [  1.72000000e+02   3.27100000e+03]
 [  1.73000000e+02   3.29000000e+03]
 [  1.74000000e+02   3.30900000e+03]
 [  1.75000000e+02   3.32800000e+03]
 [  1.76000000e+02   3.34700000e+03]
 [  1.77000000e+02   3.36600000e+03]
 [  1.78000000e+02   3.38500000e+03]
 [  1.79000000e+02   3.40400000e+03]
 [  1.80000000e+02   3.42300000e+03]
 [  1.81000000e+02   3.44200000e+03]
 [  1.82000000e+02   3.46100000e+03]
 [  1.83000000e+02   3.48000000e+03]
 [  1.84000000e+02   3.49900000e+03]
 [  1.85000000e+02   3.51800000e+03]
 [  1.86000000e+02   3.53700000e+03]
 [  1.87000000e+02   3.55600000e+03]
 [  1.88000000e+02   3.57500000e+03]
 [  1.89000000e+02   3.59400000e+03]
 [  1.90000000e+02   3.61300000e+03]
 [  1.91000000e+02   3.63200000e+03]
 [  1.92000000e+02   3.65100000e+03]
 [  1.93000000e+02   3.67000000e+03]
 [  1.94000000e+02   3.68900000e+03]
 [  1.95000000e+02   3.70800000e+03]
 [  1.96000000e+02   3.72700000e+03]
 [  1.97000000e+02   3.74600000e+03]
 [  1.98000000e+02   3.76500000e+03]
 [  1.99000000e+02   3.78400000e+03]]

Process finished with exit code 0

```

If so, you have just ran the sPyNNaker front end and used 3 external algorithms (RigRouter,RigCommandLineHilbertPlacer,RigAllocator). Now try creating your own algorithms and xml files and start experimenting.


# <a name="Trouble"></a> Troubleshooting

no issues have come about yet.