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
use of new mapping algorithms to use with the SpiNNaker tool chain. This functionality allows algorithms coded in any language to be used in conjunction with the tool chain through the use of XML and JSON files.

**NB:** Updating this part of the software is for advanced users only; you can break your installation of the SpiNNaker tool chain quite profoundly if you get it truly wrong. 

## <a name="Requirements"></a> Requirements

To use this functionality, you must have installed one of the Front Ends supported by the
software stack. If you have not done so yet, please follow one of the following links:

1. [The sPyNNaker Front end User installation page](/spynnaker/4.0.0/PyNNOnSpinnakerInstall.html)
1. [The SpiNNaker Graph Front End User installation page](/graph_front_end/4.0.0/SpiNNakerGraphFrontEndInstall.html)

# <a name="XMLMeta"></a> Algorithm Meta-data XML File

As end users can add any arbitrary number of algorithms to the PACMAN flow, 
this means there is no longer a predefined logic flow between algorithms. 
To rectify this, there is a block of code located in https://github.com/SpiNNakerManchester/PACMAN/blob/4.0.0/pacman/executor/pacman_algorithm_executor.py which takes a description of the inputs, outputs, and executable parameters of the algorithms available to it and a list of algorithms which it needs to execute and deduces the logical order of algorithms.

Any new algorithm needs to have a XML file which states how to execute the algorithm, its inputs and outputs. Below is an example XML file:

## Example

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

This example XML shows 2 algorithm descriptions (the BasicPartitioner which is an internal algorithm for PACMAN and an external placing algorithm known as RigCommandLineSAPlacer) All algorithms defined in this file must reside between the `<algorithms>` tag, and each algorithm needs to be encapsulated between `<algorithm>` tags. Each Algorithm has a name (referred to by the `<algorithm name=>` tag) which is used during configuration to identify what algorithms to run. Below is a breakdown of how this XML file describes the two algorithms.

The BasicPartitioner takes 2 parameters as its inputs, which are defined by the parameters encapsulated within the `<required_inputs>`, `<param_name>` and `<param_type>` tags. These are:

1. The partitionable graph which has a type of MemoryPartitionableGraph for clarity,
1. and a python representation of the SpiNNaker machine which has been extended to represent external devices as virtual chips, and which has a type of MemoryExtendedMachine for clarity.

The BasicPartitioner generates 2 outputs, which are defined by the parameters encapsulated within the `<produces_outputs>`, `<param_name>` and `<param_type>` tags. These are:

1. The partitioned graph contains vertices (referred to as "partitioned vertices") each of which contains all or a subset of the atoms from a vertex in the partitionable graph. Each of these partitioned vertices represents what is supported by a core in the SpiNNaker machine.
1. and a mapping between the partitionable and partitioned graph, known as a graph mapper which has a type of MemoryGraphMapper for clarity.

Because the BasicPartitioner is a internal algorithm of PACMAN and therefore uses the PACMAN data structures, it can be run directly as a imported Python module. Therefore the tool chain needs to know where the module lives (in relation to the PACMAN install) and what class to instantiate and call. These pieces of data can be found in the `<python_module>` and `<python_class>` tags.

The RigCommandLineSAPlacer on the other hand is a external algorithm to PACMAN and therefore has to be run as a command runnable from the command line. The RigCommandLineSAPlacer takes 5 parameters as its command line inputs, and requires 2 commands to run. These are encapsulated within the `<command_line_args>` and `<arg>` tags. These arguments are as follows:

The first and second arguments state that it's a Python class to run, and the path required to make the script run from the command line. Here we have assumed that the script can be ran directly from anywhere. The rest of the arguments correspond to inputs to the algorithm and are tied to the `<required_inputs>` tags. These are described below:

1. The algorithm to use. This algorithm is a interface for a collection of placers and because the tool chain can only process each algorithm individually. This means in this case that it is hard coded and therefore is not needed in the `<required_inputs>` tags.
1. A file representation of the PACMAN's `partitioned_graph` is required under the parameter `--graph`. This is deduced from the required input, which has the `parameter_name` of `graph` and type of `FilePartitionedGraph`.
1. A file representation of the SpiNNaker machine is required under the parameter `--machine`. This is deduced from the required input, which has the `parameter_name` of `machine` and type `FileMachine`.
1. A file that contains constraints on vertices within the partitioned graph is required under the parameter `--constraints`. This is deduced from the required input, which has the `parameter_name` of `constraints` and type `FileConstraints`.
1. A file path for where to write the output JSON file for its FilePlacements is required under the parameter `--placements`. This is deduced from the required input, which has the name `placements_path` and has the type `FilePlacementFilePath`.

The RigCommandLineSAPlacer also produces one output, which is the JSON file which contains placement information. This is deduced from the `<produces_outputs>` tags. Note that the `para_name` is the same as the input type for the `placements_path`. This allows the PACMAN algorithm to deduce what type of data your outputting, whilst supporting general naming of output files.

## Predefined Types and Algorithms 

The tool chain currently supplies a collection of inputs into the PACMAN infrastructure. These are defined below:

|Name|Definition|
|:----------------|:-----------------|
|`MemoryPartitionableGraph`|The Python object for the partitionable graph|
|`MemoryMachine`|The Python object of the spiNNaker machine|
|`ReportFolder`|The file path for where to write reports|
|`IPAddress`|The IP address for the SpiNNaker machine|
|`Transceiver`|The Python interface to the SpiNNaker machine|
|`FileCoreAllocationsFilePath`|The file path for writing core allocations|
|`FileSDRAMAllocationsFilePath`|The file path for writing SDRAM allocations|
|`FileMachineFilePath`|The file path for writing the JSON representation of the SpiNNaker machine produced by PACMAN|
|`FilePartitionedGraphFilePath`|The file path for writing the JSON representation of the partitioned graph produced by PACMAN|
|`FilePlacementFilePath`|The file path for writing the JSON representation of the placements produced by PACMAN|
|`FileRoutingPathsFilePath`|The file path for writing the JSON representation of the routing paths|
|`FileConstraintsFilePath`|The file path for writing the JSON representation of the constraints from the partitioned graph|

The tool chain also provides a collection of converters which switch between json file formats and PACMAN'S data objects. These are summarised below:

|Name|Definition|Inputs|Outputs|Currently Implemented?|
|:----------|:----------------------------|:------------|:------------|:-------|
|`ConvertToFilePlacement`|Converts from PACMAN placements to Json Placements| MemoryPlacements, FilePlacementFilePath| FilePlacements| True|
|`ConvertToFilePartitionedGraph`|Converts from PACMAN partitioned graph to Json partitioned graph| MemoryPartitionedGraph, FilePartitionedGraphFilePath| FilePartitionedGraph| True|
|`ConvertToFileCoreAllocation`|Converts PACMAN placements to the Json core_allocations| MemoryPlacements, FileCoreAllocationsFilePath| FileCoreAllocations| True|
|`ConvertToFileMachine`|Converts from the PACMAN machine object to the Json Machine| MemoryMachine, FileMachineFilePath|FileMachine| True|
|`CreateToFileConstraints`|Creates the Json constraints file from PACMAN machine with virtual chips and the PACMAN partitioned graph| MemoryExtendedMachine, MemoryPartitionedGraph, FileConstraintsFilePath| FileConstraints| True|
|`ConvertToFilePartitionableGraph`|Converts from PACMAN partition able graph to Json partition able graph| MemoryPartitionableGraph, FilePartitionableGraphFilePath|FilePartitionableGraph| False|
|`ConvertToFileRoutingTables`|Converts PACMAN routing tables into Json routing tables| MemoryRoutingTables, FileRoutingTablesFilePath|FileRoutingTables| False|
|`ConvertToMemoryPlacements`|Converts from the Json placement, core_allocation to the PACMAN placements, which requires PACMAN'S partitioned graph| MemoryExtendedMachine, FilePlacements, MemoryPartitionedGraph, FileCoreAllocations, FileConstraints| MemoryPlacements| True|
|`ConvertToMemoryMultiCastRoutingPaths`|Converts Json routing_paths to PACMAN routing paths with the use of PACMAN's partitioned graph, placements, and machine with virtual chips| FileRoutingPaths, MemoryPartitionedGraph, MemoryPlacements, MemoryExtendedMachine| MemoryRoutingPaths| True|
|`ConvertToMemoryRoutingTables`|Converts Json routing tables into PACMAN routing tables| FileRoutingTables|MemoryRoutingTables|False|
|`ConvertToMemoryPartitionedGraph`|Converts Json partitioned graph into PACMAN partitioned graph| FilePartitionedGraph|MemoryPartitionedGraph| False|


These extra algorithms are only used when required, and do not need to be explicitly defined in your algorithm listings.

The tool chain also uses this workflow to control when a collection of support algorithms are executed. These algorithms are summarised below:

|Name|Definition|Inputs|Outputs|Currently Implemented?|
|:----------|:----------------------------|:------------|:------------|:-------|
|`FrontEndCommonPartitionableGraph DataSpecificationWriter`|The compression of data from a partitionable graph via the data specification language| MemoryPlacements, MemoryGraphMapper, MemoryTags, ExecutableFinder, MemoryPartitionedGraph, MemoryPartitionableGraph, MemoryRoutingInfos, IPAddress, ReportFolder, WriteTextSpecsFlag, ApplicationDataFolder|DataSpecificationTargets, ExecutableTargets| True|
|`FrontEndCommonPartitionable GraphHostExecuteDataSpecification`|The decompression of data from a partitionable graph via the data specification language on host| IPAddress, MemoryPlacements, MemoryGraphMapper, ReportFolder, WriteTextSpecsFlag, ApplicationDataFolder, MemoryExtendedMachine, DataSpecificationTargets| ProcessorToAppDataBaseAddress, VertexToAppDataFilePaths| True|
|`FrontEndCommonChipExecuteDataSpecification`|The decompression of data via the data specification language on the SpiNNaker Machine itself| ?????| ????| True|
|`FrontEndCommonPartitionable GraphApplicationDataLoader`|The loading of application data from host to a SpiNNaker machine|MemoryPlacements, MemoryGraphMapper, ProcessorToAppDataBaseAddress, VertexToAppDataFilePaths, MemoryTransciever, WriteCheckerFlag| LoadedApplicationDataToken|True|
|`FrontEndCommonLoadExecutableImages` |The loading of executable binary images| ExecutableTargets, APPID, MemoryTransciever|LoadBinariesToken| True|
|`FrontEndCommonRoutingTableLoader`|The loading of routing_tables|MemoryRoutingTables, APPID, MemoryTransciever, MemoryExtendedMachine|LoadedRoutingTablesToken| True|
|`FrontEndCommonTagsLoader`|The loading of tags (iptags and reverse_ip_tags)| MemoryTags, MemoryTransciever| LoadedIPTagsToken, LoadedReverseIPTagsToken|True|
|`FrontEndCommonReloadScriptCreator`|The generation of a Reload script for reloading an application. We refer the reader to [reload_description](ReloadFunctionality.html) for more information on this functionality.| MemoryTags,ApplicationDataFolder, IPAddress, BoardVersion, BMPDetails, DownedChipsDetails, DownedCoresDetails, NumberOfBoards, MachineHeight, MachineWidth, AutoDetectBMPFlag, EnableReinjectionFlag, ProcessorToAppDataBaseAddress, MemoryPlacements, MemoryRoutingTables, MemoryExtendedMachine, ExecutableTargets, RunTime, TimeScaleFactor,DatabaseWaitOnConfirmationFlag, DatabaseSocketAddresses, VertexToAppDataFilePaths, BufferManager|ReloadToken|True|
|`FrontEndCommonApplicationRunner`|The execution of the applications on the SpiNNaker Machine|BufferManager, DatabaseWaitOnConfirmationFlag, SendStartNotifications, DatabaseInterface, ExecutableTargets, APPID, MemoryTransciever, RunTime, TimeScaleFactor, LoadedReverseIPTagsToken, LoadedIPTagsToken, LoadedRoutingTablesToken, LoadBinariesToken, LoadedApplicationDataToken| RanToken| True|
|`FrontEndCommonProvenanceGatherer`|The gathering of Provenance data from the SpiNNaker Machine|ProvenanceFilePath, MemoryTransciever, MemoryExtendedMachine, MemoryRoutingTables, MemoryPlacements| RanToken| True |
|`FrontEndCommonDatabaseWriter`|The writing of the database used by the notification protocol which supports Live input and Output. We refer the reader to [live_input/output](../spynnaker/SimpleIOLabManual.pdf) for more information on this functionality.|MemoryPartitionedGraph, UserCreateDatabaseFlag, MemoryTags, DatabaseWaitOnConfirmationFlag, ApplicationDataFolder, RunTime, MemoryExtendedMachine, DatabaseSocketAddresses, TimeScaleFactor, MachineTimeStep, MemoryPartitionableGraph, MemoryGraphMapper, MemoryPlacements, MemoryRoutingInfos, MemoryRoutingTables, ExecuteMapping| DatabaseInterface| True|
|`FrontEndCommonBufferManagerCreator`|The execution of the Buffered functionality used to support applications which require data to be sent to it from host during runtime. we refer the reader to [buffer_manager](BufferManager.html) for more information on this functionality.|MemoryPartitionedGraph, MemoryPlacements, MemoryTags, MemoryTransciever, ReportStates, ApplicationDataFolder| BufferManager| True|
|`FrontEndCommon VirtualMachineInterfacer`|The creation of the Python representation of the SpiNNaker Machine|MachineWidth, MachineHeight, MachineHasWrapAroundsFlag| MemoryMachine| True|
|`FrontEndCommon MachineInterfacer`|The creation of the python representation of the SpiNNaker Machine and the Python interface to the SpiNNaker Machine|IPAddress, BMPDetails, DownedChipsDetails, DownedCoresDetails, BoardVersion, NumberOfBoards, MachineWidth, MachineHeight, AutoDetectBMPFlag, EnableReinjectionFlag, ScampConnectionData, BootPortNum| MemoryMachine, MemoryTransciever| True|

These algorithms use a collection of Tokens to define which functions depend upon each other. These tokens are usually the output from each function; they are summarised below for clarity:

|Name|Definition of Generation Condition|
|:----------------|:-----------------|
|`RanToken`| The simulation on the SpiNNaker machine.|
|`LoadedApplicationDataToken`| The data needed by the application has been loaded into the SDRAM of the SpiNNaker machine.|
|`LoadBinariesToken`| The application binaries have been loaded onto the SpiNNaker machine.|
|`ReloadToken`| The reload script has been built.|
|`LoadedRoutingTablesToken`| The routing tables have been loaded onto the SpiNNaker machine.|
|`LoadedReverseIPTagsToken`| The reverse iptags have been loaded onto the Ethernet connected chips on the SpiNNaker machine.|
|`LoadedIPTagsToken`| The iptags have been loaded onto the Ethernet connected chips on the SpiNNaker machine.|

The tool chain expects to be able to extract a number of PACMAN objects at the end of the algorithm execution. This is mainly for transmitting the objects onto the SpiNNaker machine, and supporting data retrieval later-on. These objects are as follows:

|Name|Definition|
|:----------------|:-----------------|
|`MemoryPlacements`| The PACMAN representation of the placements. |
|`MemoryRoutingTables`| The PACMAN representation of the entries used on each routing table.|
|`MemoryRoutingInfos`| The PACMAN representation of the keys and masks allocated to each edge in the partitioned graph.|
|`MemoryTags`| The PACMAN representation of the tags allocated to the sub-vertices of the partitioned graph.|
|`MemoryPartitionedGraph`| The PACMAN representation of the partitioned graph.|
|`MemoryGraphMapper`| The PACMAN representation of the mapping between partition able and partitioned graphs.|
|`RanToken`| The Token that states that the simulation executed on the SpiNNaker machine.|

# <a name="Json"></a> JSON File Format

We refer you to the documentation on the JSON File Format found [here](https://github.com/mossblaser/place-and-route-interchange-format)

# <a name="Configuration"></a> Configuration

To configure the sPyNNaker front end to use your algorithms, you must first have the XML file mentioned in [Algorithm Meta-data XML File](#XMLMeta) for your algorithm and have added the Json converters to your algorithm's front end. Then you will need to open your `.spynnaker.cfg` file and add these extra regions and params.

    [Mapping]
    application_to_machine_graph_algorithms = PartitionAndPlacePartitioner
    machine_graph_to_machine_algorithms = GraphEdgeFilter,OneToOnePlacer,RigRoute,BasicTagAllocator,FrontEndCommonEdgeToNKeysMapper,MallocBasedRoutingInfoAllocator,BasicRoutingTableGenerator,MundyRouterCompressor


    # format is <path1>,<path2>
    extra_xmls_paths = None

At this point, you need to :

1. Remove the PACMAN specific algorithm that your algorithm replaces.
1. Add your algorithms name (as specified in the `<algorithm name="">` tag) to the list.
1. add a path to your XML file containing its input and output data in the "`extra_xml_paths`"
1. If the algorithm loads one of the objects onto the machine that the interface algorithms, you may be able to return one of the tokens described in # and therefore remove the corresponding interface function from the interface_algorithms list.
1. run a pynn script.

# <a name="RigPlacer"></a> Running Example

To run a simple example of using external and internal algorithms, please follow these instructions:

1. Install rig (this can be done via the command pip install rig)
2. `git clone https://github.com/mossblaser/place-and-route-interchange-format.git`
3. Create a XML file with the following data:

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

4. Replace `PATH_TO_GIT_CLONE` in the xml file with the absolute path to the git clone from before.
5. Modify your `.spynnaker.cfg` file to include the following lines:

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

6. Replace `PATH_TO_XML_FILE` with a absolute path to the XML file you just wrote.
7. Download (PyNN7Examples)[https://github.com/SpiNNakerManchester/PyNN7Examples] (if using PyNN 0.7) or (PyNN8Examples)[https://github.com/SpiNNakerManchester/PyNN7Examples] (if using PyNN 0.8)
8. Run the python script `examples/synfire_if_curr_exp.py`

You should now see some progress bars and timings indicating that it has just run these algorithms.  If so, you have just run the sPyNNaker front end and used 3 external algorithms (RigRouter,RigCommandLineHilbertPlacer,RigAllocator). Now try creating your own algorithms and XML files and start experimenting.
