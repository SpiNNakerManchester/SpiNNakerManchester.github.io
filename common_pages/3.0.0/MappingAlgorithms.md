---
title: Adding new mapping algorithms to the SpiNNaker tool-chain
published: true
---
# The version described here is no longer supported. 

[Home page for current version](/) 


# Contents
* [Usage](#Usage)
* [Requirements](#Requirements)
* [Algorithm Meta-data XML File](#XMLMeta)
* [Json File Format](#Json)
* [Configuration](#Configuration)
* [Running Example](#RigPlacer)
* [Troubleshooting](#Trouble)

# <a name="Usage"></a> Usage of this functionality

The content of this page is to support end users whom wish to investigate the 
use of new mapping algorithms to use with the SpiNNaker tool chain.

This functionality allows algorithms coded in any language to be used in conjunction with the tool chain through the use of XML and json files.


# <a name="Requirements"></a> Requirements

To use this functionality, you must have installed one of the Front Ends supported by the
software stack. If you have not done so yet, please follow one of the following links:

1. [The sPyNNaker Front end User installation page](/spynnaker/3.0.0/PyNNOnSpinnakerInstall.html)
1. [The SpiNNaker Graph Front End User installation page](/graph_front_end/3.0.0/SpiNNakerGraphFrontEndInstall.html)

# <a name="XMLMeta"></a> Algorithm Meta-data XML File

As end users can add any arbitrary number of algorithms to the PACMAN flow, 
this means there is no longer a predefined logic flow between algorithms. 
To rectify this, there is a block of code located in https://github.com/SpiNNakerManchester/PACMAN/blob/3.0.0/pacman/executor/pacman_algorithm_executor.py which takes a description of the inputs, outputs, and executable parameters of the algorithms available to it and a list of algorithms which it needs to execute and deduces the logical order of algorithms.

Any new algorithm needs to have a XML file which states how to execute the algorithm, its inputs and outputs. Below is an example XML file:

```xml
<algorithms>
    <algorithm name="BasicPartitioner">
        <python_module>pacman.operations.partition_algorithms.basic_partitioner</python_module>
        <python_class>BasicPartitioner</python_class>
        <input_definitions>
            <parameter>
                <param_name>graph</param_name>
                <param_type>MemoryPartitionableGraph</param_type>
            </parameter>
            <parameter>
                <param_name>machine</param_name>
                <param_type>MemoryExtendedMachine</param_type>
            </parameter>
        </input_definitions>
        <required_inputs>
            <param_name>graph</param_name>
            <param_name>machine</param_name>
        </required_inputs>
        <outputs>
            <param_type>MemoryPartitionedGraph</param_type>
            <param_type>MemoryGraphMapper</param_type>
        </outputs>
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
        <input_definitions>
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
        </input_definitions>
        <required_inputs>
            <param_name>graph</param_name>
            <param_name>machine</param_name>
            <param_name>constraints</param_name>
            <param_name>placements_path</param_name>
        </required_inputs>
        <outputs>
            <param_type file_name_type="FilePlacementsFilePath">
                FilePlacements
            </param_type>
        </outputs>
    </algorithm>
</algorithms>
```

This example XML shows 2 algorithm descriptions (the BasicPartitioner which is an internal algorithm for PACMAN and an external placing algorithm known as RigCommandLineSAPlacer) All algorithms defined in this file must reside between the ```<algorithms>``` tag, and each algorithm needs to be encapsulated between ```<algorithm>``` tags. Each Algorithm has a name (referred to by the <algorithm name=> tag) which is used during configuration to identify what algorithms to run. Below is a breakdown of how this XML file describes the two algorithms.

The BasicPartitioner takes 2 parameters as its inputs, which are defined by the parameters encapsulated within the ```<required_inputs>, <param_name> and <param_type>``` tags. These are:

1. The partitionable graph which has a type of MemoryPartitionableGraph for clarity,
1. and a python representation of the SpiNNaker machine which has been extended to represent external devices as virtual chips, and which has a type of MemoryExtendedMachine for clarity.
 
The BasicPartitioner generates 2 outputs, which are defined by the parameters encapsulated within the ```<produces_outputs>, <param_name> and <param_type>``` tags. These are:

1. The partitioned graph contains vertices (referred to as "partitioned vertices") each of which contains all or a subset of the atoms from a vertex in the partitionable graph. Each of these partitioned vertices represents what is supported by a core in the SpiNNaker machine.
1. and a mapping between the partitionable and partitioned graph, known as a graph mapper which has a type of MemoryGraphMapper for clarity.
 
Because the BasicPartitioner is a internal algorithm of PACMAN and therefore uses the PACMAN data structures, it can be run directly as a imported python module. Therefore the tool chain needs to know where the module lives (in relation to the PACMAN install) and what class to instantiate and call. These pieces of data can be found in the ```<python_module> and <python_class>``` tags.

The RigCommandLineSAPlacer on the other hand is a external algorithm to PACMAN and therefore has to be run as a command runnable from the command line. The RigCommandLineSAPlacer takes 5 parameters as its command line inputs, and requires 2 commands to run. These are encapsulated within the ```<command_line_args> and <arg> ``` tags. These arguments are as follows:

The first and second arguments state that it's a python class to run, and the path required to make the script run from the command line. Here we have assumed that the script can be ran directly from anywhere. The rest of the arguments correspond to inputs to the algorithm and are tied to the ```<required_inputs>``` tags. These are described below:

1. The algorithm to use. This algorithm is a interface for a collection of placers and because the tool chain can only process each algorithm individually. This means in this case that it is hard coded and therefore is not needed in the ```<required_inputs>``` tags.
1. A file representation of the PACMAN's partitioned_graph is required under the parameter --graph. This is deduced from the required input, which has the parameter_name of graph and type of FilePartitionedGraph.
1. A file representation of the SpiNNaker machine is required under the parameter --machine. This is deduced from the required input, which has the parameter_name of machine and type FileMachine.
1. A file that contains constraints on vertices within the partitioned graph is required under the parameter --constraints. This is deduced from the required input, which has the parameter_name of constraints and type FileConstraints.
1. A file path for where to write the output json file for its FilePlacements is required under the parameter --placements. This is deduced from the required input, which has the name placements_path and has the type FilePlacementFilePath.

The RigCommandLineSAPlacer also produces one output, which is the json file which contains placement information. This is deduced from the ```<produces_outputs>``` tags. Note that the para_name is the same as the input type for the placements_path. This allows the PACMAN algorithm to deduce what type of data your outputting, whilst supporting general naming of output files. 

The tool chain currently supplies a collection of inputs into the PACMAN infrastructure. These are defined below:

|Name|Definition|
|:----------------|:-----------------|
|MemoryPartitionableGraph|python object for the partition able graph|
|MemoryMachine|python object of the SpiNNaker machine|
|ReportFolder|the file-path for where to write reports|
|MemoryPartitionableGraph|python object for the partitionable graph|
|MemoryMachine|python object of the spiNNaker machine|
|ReportFolder|the file path for where to write reports|
|IPAddress|the ip address for the SpiNNaker machine|
|Transceiver| the python interface to the SpiNNaker machine|
|FileCoreAllocationsFilePath|the file path for writing core allocations|
|FileSDRAMAllocationsFilePath|the file path for writing sdram allocations|
|FileMachineFilePath|the file path for writing the json representation of the SpiNNaker machine produced by PACMAN|
|FilePartitionedGraphFilePath|the file path for writing the json representation of the partitioned graph produced by PACMAN| 
|FilePlacementFilePath|the file path for writing the json representation of the placements produced by PACMAN|
|FileRoutingPathsFilePath|the file path for writing the json representation of the routing paths|
|FileConstraintsFilePath|the file path for writing the json representation of the constraints from the partitioned graph|


The tool chain also provides a collection of converters which switch between json file formats and PACMAN'S data objects. These are summarised below:

|Name|Definition|Inputs|Outputs|Currently Implemented?|
|:----------|:----------------------------|:------------|:------------|:-------|
|ConvertToFilePlacement|Converts from PACMAN placements to Json Placements| MemoryPlacements, FilePlacementFilePath| FilePlacements| True|
|ConvertToFilePartitionedGraph|Converts from PACMAN partitioned graph to Json partitioned graph| MemoryPartitionedGraph, FilePartitionedGraphFilePath| FilePartitionedGraph| True|
|ConvertToFileCoreAllocation|Converts PACMAN placements to the Json core_allocations| MemoryPlacements, FileCoreAllocationsFilePath| FileCoreAllocations| True|
|ConvertToFileMachine|Converts from the PACMAN machine object to the Json Machine| MemoryMachine, FileMachineFilePath|FileMachine| True|
|CreateToFileConstraints|Creates the Json constraints file from PACMAN machine with virtual chips and the PACMAN partitioned graph| MemoryExtendedMachine, MemoryPartitionedGraph, FileConstraintsFilePath| FileConstraints| True|
|ConvertToFilePartitionableGraph|Converts from PACMAN partition able graph to Json partition able graph| MemoryPartitionableGraph, FilePartitionableGraphFilePath|FilePartitionableGraph| False|
|ConvertToFileRoutingTables|Converts PACMAN routing tables into Json routing tables| MemoryRoutingTables, FileRoutingTablesFilePath|FileRoutingTables| False|
|ConvertToMemoryPlacements|Converts from the Json placement, core_allocation to the PACMAN placements, which requires PACMAN'S partitioned graph| MemoryExtendedMachine, FilePlacements, MemoryPartitionedGraph, FileCoreAllocations, FileConstraints| MemoryPlacements| True|
|ConvertToMemoryMultiCastRoutingPaths|Converts Json routing_paths to PACMAN routing paths with the use of PACMAN's partitioned graph, placements, and machine with virtual chips| FileRoutingPaths, MemoryPartitionedGraph, MemoryPlacements, MemoryExtendedMachine| MemoryRoutingPaths| True|
|ConvertToMemoryRoutingTables|Converts Json routing tables into PACMAN routing tables| FileRoutingTables|MemoryRoutingTables|False|
|ConvertToMemoryPartitionedGraph|Converts Json partitioned graph into PACMAN partitioned graph| FilePartitionedGraph|MemoryPartitionedGraph| False|


These extra algorithms are only used when required, and are not needed to be explicitly defined in your algorithm listings.

The tool chain also uses this workflow to control when a collection of support algorithms are executed. These algorithms are summarised below:

|Name|Definition|Inputs|Outputs|Currently Implemented?|
|:----------|:----------------------------|:------------|:------------|:-------|
|FrontEndCommonPartitionableGraph DataSpecificationWriter |The compression of data from a partitionable graph via the data specification language| MemoryPlacements, MemoryGraphMapper, MemoryTags, ExecutableFinder, MemoryPartitionedGraph, MemoryPartitionableGraph, MemoryRoutingInfos, IPAddress, ReportFolder, WriteTextSpecsFlag, ApplicationDataFolder|DataSpecificationTargets, ExecutableTargets| True|
|FrontEndCommonPartitionable GraphHostExecuteDataSpecification|The decompression of data from a partitionable graph via the data specification language on host| IPAddress, MemoryPlacements, MemoryGraphMapper, ReportFolder, WriteTextSpecsFlag, ApplicationDataFolder, MemoryExtendedMachine, DataSpecificationTargets| ProcessorToAppDataBaseAddress, VertexToAppDataFilePaths| True|
|FrontEndCommonChipExecuteDataSpecification |The decompression of data via the data specification language on the SpiNNaker Machine itself| ?????| ????| True|
|FrontEndCommonPartitionable GraphApplicationDataLoader|The loading of application data from host to a SpiNNaker machine|MemoryPlacements, MemoryGraphMapper, ProcessorToAppDataBaseAddress, VertexToAppDataFilePaths, MemoryTransciever, WriteCheckerFlag| LoadedApplicationDataToken|True|
|FrontEndCommonLoadExecutableImages |The loading of executable binary images| ExecutableTargets, APPID, MemoryTransciever|LoadBinariesToken| True|
|FrontEndCommonRoutingTableLoader |The loading of routing_tables|MemoryRoutingTables, APPID, MemoryTransciever, MemoryExtendedMachine|LoadedRoutingTablesToken| True|
|FrontEndCommonTagsLoader |The loading of tags (iptags and reverse_ip_tags)| MemoryTags, MemoryTransciever| LoadedIPTagsToken, LoadedReverseIPTagsToken|True|
|FrontEndCommonReloadScriptCreator |The generation of a Reload script for reloading an application. We refer the reader to [reload_description](ReloadFunctionality.html) for more information on this functionality.| MemoryTags,ApplicationDataFolder, IPAddress, BoardVersion, BMPDetails, DownedChipsDetails, DownedCoresDetails, NumberOfBoards, MachineHeight, MachineWidth, AutoDetectBMPFlag, EnableReinjectionFlag, ProcessorToAppDataBaseAddress, MemoryPlacements, MemoryRoutingTables, MemoryExtendedMachine, ExecutableTargets, RunTime, TimeScaleFactor,DatabaseWaitOnConfirmationFlag, DatabaseSocketAddresses, VertexToAppDataFilePaths, BufferManager|ReloadToken|True|
|FrontEndCommonApplicationRunner |The execution of the applications on the SpiNNaker Machine|BufferManager, DatabaseWaitOnConfirmationFlag, SendStartNotifications, DatabaseInterface, ExecutableTargets, APPID, MemoryTransciever, RunTime, TimeScaleFactor, LoadedReverseIPTagsToken, LoadedIPTagsToken, LoadedRoutingTablesToken, LoadBinariesToken, LoadedApplicationDataToken| RanToken| True|
| FrontEndCommonProvenanceGatherer|The gathering of Provenance data from the SpiNNaker Machine|ProvenanceFilePath, MemoryTransciever, MemoryExtendedMachine, MemoryRoutingTables, MemoryPlacements| RanToken| True |
|FrontEndCommonDatabaseWriter |The writing of the database used by the notification protocol which supports Live input and Output. We refer the reader to [live_input/output](../spynnaker/SimpleIOLabManual.pdf) for more information on this functionality.|MemoryPartitionedGraph, UserCreateDatabaseFlag, MemoryTags, DatabaseWaitOnConfirmationFlag, ApplicationDataFolder, RunTime, MemoryExtendedMachine, DatabaseSocketAddresses, TimeScaleFactor, MachineTimeStep, MemoryPartitionableGraph, MemoryGraphMapper, MemoryPlacements, MemoryRoutingInfos, MemoryRoutingTables, ExecuteMapping| DatabaseInterface| True|
|FrontEndCommonBufferManagerCreator |The execution of the Buffered functionality used to support applications which require data to be sent to it from host during runtime. we refer the reader to [buffer_manager](BufferManager.html) for more information on this functionality.|MemoryPartitionedGraph, MemoryPlacements, MemoryTags, MemoryTransciever, ReportStates, ApplicationDataFolder| BufferManager| True|
|FrontEndCommon VirtualMachineInterfacer |The creation of the Python representation of the SpiNNaker Machine|MachineWidth, MachineHeight, MachineHasWrapAroundsFlag| MemoryMachine| True|
|FrontEndCommon MachineInterfacer |The creation of the python representation of the SpiNNaker Machine and the Python interface to the SpiNNaker Machine|IPAddress, BMPDetails, DownedChipsDetails, DownedCoresDetails, BoardVersion, NumberOfBoards, MachineWidth, MachineHeight, AutoDetectBMPFlag, EnableReinjectionFlag, ScampConnectionData, BootPortNum| MemoryMachine, MemoryTransciever| True|

These algorithms use a collection of Tokens to define which functions depend upon each other. These tokens are usually the output from each function. But are summarised below for clarity:

|Name|Definition|
|:----------------|:-----------------|
|RanToken| states that the algorithm has ran the simulation on the SpiNNaker machine.|
|LoadedApplicationDataToken| States that the algorithm has loaded the data needed by the application onto the SDRAM of the SpiNNaker Machine|
|LoadBinariesToken| States that the algorithm has loaded the application binaries onto the SpiNNaker Machine|
|ReloadToken| States that the reload script has been built|
|LoadedRoutingTablesToken| States that the routing tables have been loaded onto the chips of the SpiNNaker Machine|
|LoadedReverseIPTagsToken| States that the reverse iptags have been loaded to the Ethernet connected chips on the SpiNNaker Machine|
|LoadedIPTagsToken| States that the iptags have been loaded to the Ethernet connected chips on the SpiNNaker Machine|


The tool chain expects to be able to extract a number of PACMAN objects at the end of the algorithm execution. This is mainly for transmitting the objects onto the SpiNNaker machine, and supporting data retrieval later-on. These objects are as follows:

|Name|Definition|
|:----------------|:-----------------|
|MemoryPlacements| The PACMAN representation of the placements. |
|MemoryRoutingTables| The PACMAN representation of the entries used on each routing table.|
|MemoryRoutingInfos| The PACMAN representation of the keys and masks allocated to each edge in the partitioned graph.|
|MemoryTags| The PACMAN representation of the tags allocated to the sub-vertices of the partitioned graph.|
|MemoryPartitionedGraph| The PACMAN representation of the partitioned graph.|
|MemoryGraphMapper| The PACMAN representation of the mapping between partition able and partitioned graphs.|
|RanToken| The Token that states that the simulation executed on the SpiNNaker machine|


# <a name="Json"></a> Json File Format

we refer you to the documentation on the Json File Format found [here](https://github.com/mossblaser/place-and-route-interchange-format)

# <a name="Configuration"></a> Configuration

To configure the sPyNNaker front end to use your algorithms, you must first have the XML file mentioned in [Algorithm Meta-data XML File](#XMLMeta) for your algorithm and have added the Json converters to your algorithm's front end. Then you will need to open your .spynnaker.cfg file and add these extra regions and params.

    [Mapping]
    application_to_machine_graph_algorithms = PartitionAndPlacePartitioner
    machine_graph_to_machine_algorithms = GraphEdgeFilter,OneToOnePlacer,RigRoute,BasicTagAllocator,FrontEndCommonEdgeToNKeysMapper,MallocBasedRoutingInfoAllocator,BasicRoutingTableGenerator,MundyRouterCompressor

    
    # format is <path1>,<path2>
    extra_xmls_paths = None

At this point, you need to :

1. Remove the PACMAN specific algorithm that you'r algorithm replaces.
1. Add your algorithms name (as specified in the ```<algorithm name="">``` tag) to the list.
1. add a path to your XML file containing its input and output data in the "extra_xml_paths"
1. If the algorithm loads one of the objects onto the machine that the interface algorithms, you may be able to return one of the tokens described in # and therefore remove the corresponding interface function from the interface_algorithms list.
1. run a pynn script.

# <a name="RigPlacer"></a> Running Example

To run a simple example of using external and internal algorithms in situ, please follow these instructions:

1. install rig (this can be done via the command pip install rig)
2. git clone https://github.com/mossblaser/place-and-route-interchange-format.git
3. create a XML file with the following data:

```xml
<algorithms>
    <algorithm name="RigCommandLineSAPlacer">
        <command_line_args>
            <arg>rig_place.py</arg>
            <arg>--algorithm=sa</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements_path}</arg>
        </command_line_args>
        <input_definitions>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FileMachineGraph</param_type>
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
                <param_type>FilePlacementsFilePath</param_type>
            </parameter>
        </input_definitions>
        <required_inputs>
            <param_name>graph</param_name>
            <param_name>machine</param_name>
            <param_name>constraints</param_name>
            <param_name>placements_path</param_name>
        </required_inputs>
        <outputs>
            <param_type file_name_type="FilePlacementsFilePath">
                FilePlacements
            </param_type>
        </outputs>
    </algorithm>
    <algorithm name="RigCommandLineHilbertPlacer">
        <command_line_args>
            <arg>rig_place.py</arg>
            <arg>--algorithm=hilbert</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements_path}</arg>
        </command_line_args>
        <input_definitions>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FileMachineGraph</param_type>
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
                <param_type>FilePlacementsFilePath</param_type>
            </parameter>
        </input_definitions>
        <required_inputs>
            <param_name>graph</param_name>
            <param_name>machine</param_name>
            <param_name>constraints</param_name>
            <param_name>placements_path</param_name>
        </required_inputs>
        <outputs>
            <param_type file_name_type="FilePlacementsFilePath">
                FilePlacements
            </param_type>
        </outputs>
    </algorithm>
    <algorithm name="RigCommandLineRandomPlacer">
        <command_line_args>
            <arg>rig_place.py</arg>
            <arg>--algorithm=rand</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements_path}</arg>
        </command_line_args>
        <input_definitions>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FileMachineGraph</param_type>
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
                <param_type>FilePlacementsFilePath</param_type>
            </parameter>
        </input_definitions>
        <required_inputs>
            <param_name>graph</param_name>
            <param_name>machine</param_name>
            <param_name>constraints</param_name>
            <param_name>placements_path</param_name>
        </required_inputs>
        <outputs>
            <param_type file_name_type="FilePlacementsFilePath">
                FilePlacements
            </param_type>
        </outputs>
    </algorithm>
    <algorithm name="RigAllocator">
        <command_line_args>
            <arg>rig_allocate.py</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements}</arg>
            <arg>--algorithm=greedy</arg>
            <arg>--allocations=cores:{core_allocation_path}</arg>
            <arg>--allocations=sdram:{sdram_allocation_path}</arg>
        </command_line_args>
        <input_definitions>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FileMachineGraph</param_type>
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
        </input_definitions>
        <required_inputs>
            <param_name>graph</param_name>
            <param_name>machine</param_name>
            <param_name>constraints</param_name>
            <param_name>placements</param_name>
            <param_name>core_allocation_path</param_name>
            <param_name>sdram_allocation_path</param_name>
        </required_inputs>
        <outputs>
            <param_type file_name_type="FileCoreAllocationsFilePath">
                FileCoreAllocations
            </param_type>
            <param_type file_name_type="FileSDRAMAllocationsFilePath">
                FileSDRAMAllocations
            </param_type>
        </outputs>
    </algorithm>
    <algorithm name="RigRouter">
        <command_line_args>
            <arg>rig_route.py</arg>
            <arg>--graph={graph}</arg>
            <arg>--constraints={constraints}</arg>
            <arg>--machine={machine}</arg>
            <arg>--placements={placements}</arg>
            <arg>--allocations=cores:{allocations}</arg>
            <arg>--algorithm=ner</arg>
            <arg>--core-resource=cores</arg>
            <arg>--routes={routing_paths_file_path}</arg>
        </command_line_args>
        <input_definitions>
            <parameter>
                <param_name>graph</param_name>
                <param_type>FileMachineGraph</param_type>
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
                <param_type>FileRoutingPathsFilePath</param_type>
            </parameter>
        </input_definitions>
        <required_inputs>
            <param_name>graph</param_name>
            <param_name>machine</param_name>
            <param_name>constraints</param_name>
            <param_name>placements</param_name>
            <param_name>allocations</param_name>
            <param_name>routing_paths_file_path</param_name>
        </required_inputs>
        <outputs>
            <param_type file_name_type="FileRoutingPathsFilePath">
                FileRoutingPaths
            </param_type>
        </outputs>
    </algorithm>
</algorithms>
```

4. Replace PATH_TO_GIT_CLONE in the xml file with the absolute path to the git clone from before.
5. modify your .spynnaker.cfg file to include the following lines:

```
[Mapping]

# format is  <algorithm_name>,<>
# pacman algorithms are:
# Basic_dijkstra_routing, RadialPlacer, BasicPlacer, ConnectiveBasedPlacer,
# BasicTagAllocator, BasicPartitioner, PartitionAndPlacePartitioner,
# BasicRoutingInfoAllocator, BasicDijkstraRouting,
# MallocBasedRoutingInfoAllocator, GraphEdgeFilter, EdgeToNKeysMapper
application_to_machine_graph_algorithms = PartitionAndPlacePartitioner
machine_graph_to_machine_algorithms = GraphEdgeFilter,RigRouter,RigCommandLineHilbertPlacer,RigAllocator,BasicTagAllocator,FrontEndCommonEdgeToNKeysMapper,MallocBasedRoutingInfoAllocator,BasicRoutingTableGenerator,MundyRouterCompressor

# format is <path1>,<path2>
extra_xmls_paths = PATH_TO_XML_FILE
```

6. replace PATH_TO_XML_FILE with a absolute path to the XML file you just wrote.
7.  (PyNNExamples)[https://github.com/SpiNNakerManchester/PyNNExamples]
8. run python PyNNExamples/examples/synfire_if_curr_exp.py

You should see output like the one below:

```
/usr/bin/python2.7 /home/S06/stokesa6/spinniker/alpha_package_103_git/PyNNExamples/examples/synfire_if_curr_exp.py
2015-10-12 12:02:13 INFO: Read config files: /home/S06/stokesa6/.spynnaker.cfg, /home/S06/stokesa6/spinniker/alpha_package_103_git/sPyNNaker/spynnaker/spynnaker.cfg, /home/S06/stokesa6/spinniker/alpha_package_103_git/spinn-6_boards_from_base.cfg
2015-10-12 12:02:14 INFO: sPyNNaker (c) 2015 APT Group, University of Manchester
2015-10-12 12:02:14 INFO: Setting time scale factor to 1.
2015-10-12 12:02:14 INFO: Setting appID to 30.
2015-10-12 12:02:14 INFO: Setting machine time step to 1000.0 micro-seconds.
2015-10-12 12:02:14 WARNING: You are trying to record the conductance from a model which does not contain conductance behaviour. You will receive current measurements instead. Sorry
2015-10-12 12:02:14 INFO: Creating transceiver for *********
2015-10-12 12:02:14 INFO: going to try to boot the machine with scamp
2015-10-12 12:02:14 INFO: Detected a machine on ip address ******** which has 5138 cores and 864 links
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

If so, you have just ran the sPyNNaker front end and used 3 external algorithms (RigRouter,RigCommandLineHilbertPlacer,RigAllocator). Now try creating your own algorithms and XML files and start experimenting.


# <a name="Trouble"></a> Troubleshooting

no issues have come about yet.
