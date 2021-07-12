---
title: Adding new mapping algorithms to the SpiNNaker tool-chain
published: true
---
This page includes many changes made since the 6.0.0 release.

# Contents
* [Usage](#Usage)
* [Requirements](#Requirements)
* [Algorithm Meta-data XML File](#XMLMeta)
* [Configuration](#Configuration)
* [Running Example](#RigPlacer)
* [Troubleshooting](#Trouble)

# <a name="Usage"></a> Usage of this functionality

The content of this page is to support end users whom wish to investigate the
use of new algorithms to use with the SpiNNaker tool chain.

**NB:** Updating this part of the software is for advanced users only; you can break your installation of the SpiNNaker tool chain quite profoundly if you get it truly wrong.

## <a name="Requirements"></a> Requirements

To use this functionality, you must have installed one of the Front Ends supported by the
software stack.
If you have not done so yet, please follow one of the following links:

1. [Developer Install](/development/index.html)
1. [The sPyNNaker Front end User installation page](/latest/spynnaker.html)
1. [The SpiNNaker Graph Front End User installation page](/latest/gfe.html)

# <a name="XMLMeta"></a> Algorithm Meta-data XML File

As end users can add any arbitrary number of algorithms to the PACMAN flow,
this means there is no longer a predefined logic flow between algorithms.
To rectify this, there is a block of code located in https://github.com/SpiNNakerManchester/PACMAN/blob/master/pacman/executor/pacman_algorithm_executor.py which takes a description of the inputs, outputs, and executable parameters of the algorithms available to it and a list of algorithms which it needs to execute and deduces the logical order of algorithms.

Any new algorithm needs to have a XML file which states how to execute the algorithm, its inputs and outputs. Below is an example XML file:

## Example

```xml
<algorithms>
    <algorithm name="ZonedRoutingInfoAllocator">
        <python_module>pacman.operations.routing_info_allocator_algorithms.zoned_routing_info_allocator</python_module>
        <python_function>flexible_allocate</python_function>
        <input_definitions>
            <parameter>
                <param_name>machine_graph</param_name>
                <param_type>MachineGraph</param_type>
            </parameter>
            <parameter>
                <param_name>n_keys_map</param_name>
                <param_type>MachinePartitionNKeysMap</param_type>
            </parameter>
        </input_definitions>
        <required_inputs>
            <param_name>machine_graph</param_name>
            <param_name>n_keys_map</param_name>
        </required_inputs>
        <optional_inputs>
            <token>EdgesFiltered</token>
        </optional_inputs>
        <outputs>
            <param_type>MemoryRoutingInfos</param_type>
        </outputs>
    </algorithm>
    <algorithm name="DSGRegionReloader">
        <python_module>spinn_front_end_common.interface.interface_functions</python_module>
        <python_class>DSGRegionReloader</python_class>
        <input_definitions>
            <parameter>
                <param_name>transceiver</param_name>
                <param_type>Transceiver</param_type>
            </parameter>
            <parameter>
                <param_name>placements</param_name>
                <param_type>Placements</param_type>
            </parameter>
            <parameter>
                <param_name>hostname</param_name>
                <param_type>IPAddress</param_type>
            </parameter>
        </input_definitions>
        <required_inputs>
            <param_name>transceiver</param_name>
            <param_name>placements</param_name>
            <param_name>hostname</param_name>
        </required_inputs>
        <optional_inputs>
            <token part="DSGDataLoaded">DataLoaded</token>
            <token>ClearedIOBuf</token>
        </optional_inputs>
        <outputs>
            <token part="DSGDataReLoaded">DataLoaded</token>
        </outputs>
    </algorithm>
</algorithms>
```

This example XML shows the ZonedRoutingInfoAllocator. 
All algorithms defined in this file must reside between the `<algorithms>` tag, and each algorithm needs to be encapsulated between `<algorithm>` tags. 
Below is a breakdown of how this XML file describes the algorithms.

Each Algorithm has a name (referred to by the `<algorithm name=>` tag) which is used during configuration to identify what algorithms to run.
Each name must be unigue.

Each Algorithm runs in a python (referred to by the `<python_module=>` tag). 
It is either done by calling the `__call__` method of a class (referred to by the `<python_class=>` tag) 
or by calling a function (referred to by the `<python_function=>` tag).
DSGRegionReloader uses the class call while ZonedRoutingInfoAllocator uses a function.

**Note:** The running of external algorithm using the `<command_line_args>` tag is no longer supported. 
Instead wrap the external algorithm in a python class/function which then calls the external algorithm, 
converting any python objects into a format the external algorithm can handle.  
Our Java based algorithm work in this way

Each aolgorithm with take zero or more input parameters. 
If required there will be one `<input_definitions>` tag, 
which contain as many `<parameter>` tags as needed, each with:  

`<param_name>` is the name the aglorithm uses in its call function.

`<param_type>` is the reference used to pass the objects between Algorithms and the Simulator.


Parameters will be either `<required_inputs>` or `<optional_inputs>`.
In either case if another algorithm outputs that parameter, that algorithm will be run first.
If nothing outputs an optional inputs it is not passed in while a missing required will raise an exception. 

ZonedRoutingInfoAllocator for example has two parameters, both required.

The ZonedRoutingInfoAllocator generates 1 output, which are defined by the parameters encapsulated within the `<outputs>` and `<param_type>` tags. 
An algorithm can provide more than one `<param_type>` by returning a tuple

There is also a `<token>` input.
These are not physical objects but do enfource order between algorithms.
They are only used when the algorithms need to run in a specific order but do not pass data as output from the first and input of the second.
Tokens are not passes in or out of the python method so they will not be in the paramters or output of the python.
They will not included in the `<input_definitions>`, but can be in `<required_inputs>`, `<optional_inputs>` or or `<outputs>`


## Predefined Types and Algorithms

Type| Class|Description|Comment|
:---|:----|:-------------|:--------|
APPID | int | The Id of the currently running applaction | [M]
ApplicationGraph | ApplicationGraph | The Graph before partitioning | [M][I]
AutoDetectBMPFlag | bool | Should the transceivver try to find a bmp | [C]
AverageCoresOnChip | float | Average number of systems cores per chip | [O]
BMPDetails | str | ip address(s) of the bmps |
BitFieldSummary | BitFieldSummary | [O] 
BoardVersion | int | version of the boards being used | [C]
BootPortNum | int | Port to connect to if not default (None)| [C][D]
BufferManager | BufferManager | Used to pass data into the cores |
CompressedRoutingTables | CompressedMulticastRoutingTable | Routing Tables after compression | [M]
CompressedSummary | RouterSummary | Summary of the routes | [O]
CompressorExecutableTargetsUsed | ExecutableTargets | aplx files used for compression | [O]
ConnectionHolders | dict(tuple(ProjectionApplicationEdge, SynapseInformation),ConnectionHolder)| connections to be returned in a PyNN-specific format |
DSGTimeMs | float | Duration of DSG for enegery calculations |
DataInMulticastKeyToChipMap | dict(tuple(int,int),int) | Chip x, y to key used for Data in |[I]
DataInMulticastRoutingTables | MulticastRoutingTables | Routes used for Data In phase | [I] 
DataNTimeSteps | int | NUmber of TimeSteps to reserve space for | [I] 
DataSpecificationTargets | DataSpecificationTargets | Core x,y,p to bytearray |
DatabaseFilePath | str or None | Path used by the DataBase interface' |
DatabaseInterface | DatabaseInterface | The interface to the database | [O]
DatabaseSocketAddresses | set(SocketAddress) | The notify_host_name, notify_port_no, listen_port of the Database |
ErrorMessages |list(str) | Errors from the Chip Io Buffer Extractor | [O]
ExecutableFinder | ExecutableFinder | Tools to find the aplx files |
ExecutableTargets | ExecutableTargets | Collectiopn of aplx files to run on cores |
ExecutableTypes | dict(ExecutableType,CoreSubsets or None) | Which cores run which ExecutableType |
ExecuteTimeMs | float | Time taken to execute for Energy calculation |
ExtendedMachine| Machine | Machine with virtual chips added (if needed) | [M]
ExtraMonitorToChipMapping | dict(tuple(int,int),ExtraMonitorSupportMachineVertex) | Map of chip x,y to Extra Monitor vertex | [M]
ExtraMonitorVertices |  list(ExtraMonitorSupportMachineVertex) | All extra monitor vertices | [M]
ExtractionTimeMs | float | Time taken to execute for Energy calculation|
FirstMachineTimeStep | int | Start timestep for this run | [I]
FixedRouteDestinationClass | Class | DataSpeedUpPacketGatherMachineVertex |
FixedRoutes | dict(tuple(int,int),FixedRouteEntry | The fixed route on each chip | [M]
GraphProvenanceItems | list(ProvenanceDataItem) | Provenance items to be writen out by ASB |
IPAddress | str | Host Name of the machine | [C]
JavaCaller | JavaCaller | Helper to call Java |
JsonMachine | str |  Json represenataion of the Machine | [O]
JsonMachineGraphPath | str | Path to where json representation of Machine graph is written | [O]
JsonPartitionNKeysMap | str | Path to where json representation of partition to n keys map is written | [O]
JsonPlacementsPath | str | Path to where json representation of the Placements is written | [O]
JsonRoutingTablesPath | str | Path to where the json representation of the Routing Tables is written [O]
LivePacketRecorderParameters |  dict(LivePacketGatherParameters, list(tuple(AbstractVertex, list(str)))) | Map of paramters to vertex and partition_ids
LivePacketRecorderParametersToVertexMapping | dict(LivePacketGatherParameters, dict(tuple(int,int),LivePacketGatherMachineVertex)) | Map of Paramteres to chip and vertex |
LoadTimeMs | float | Duration of load for enegery calculations |
MCGathererCoresToAllocate | int | number of extra Monitor cores (1) |
Machine | Machine | Machine possibly without virtual chips added | [M]
MachineAllocationController | MachineAllocationController | Spalloc |HBP control to create teh Machine |
MachineGraph | MachineGraph | graph after paritioning (if needed) | [M][I]
MachinePartitionNKeysMap | DictBasedMachinePartitionNKeysMap | Maps partitions to the keys required | [M]
MappingTimeMs | float | Duration of mapping for enegery calculations |
MaxCoresUsedOnChip | int | Max cores on a chip |[O]
MinCoresUsedOnChip | int | Min cores on a chip |[O] 
NBoardsRequired | int | Number of boards need to run job |
NChipsRequired | int | Number of chips needed to run job |
NChipsUsed | int | Number of chips used |[O] 
NSyncSteps | int | Number of timesteps between synchronisations | 
NoSyncChanges | int | number of sync changes |
NotificationInterface | NotificationProtocol | protocol for GUI and external device interaction | 
Placements | Placements | Placements by core and vertex | [M][I]
PlacementsProvenanceItems | list(ProvenanceDataItem) | Provenace data from the machine |
PlanNTimeSteps |int | Minimum number of timesteps partiting must allow |
PostSimulationOverrunBeforeError | int | timesteps to allow after run | [C]
PowerProvenanceItems | list(ProvenanceDataItem) | Provenance extracted from PowerUsed | 
PowerUsed | PowerUsed | Computed Enegery usage |
PreAllocatedResources | PreAllocatedResourceContainer | core and sdram resevations for all|ethernet chips | [M]
ProcessorToAppDataBaseAddress | dict(tuple(int,int,int), DsWriteInfo) | core (x,y,P) mapped to Data Sepec info
ProvenanceItems | list(ProvenanceDataItem) | various provenance combined by ASB |
RegionSizes | dict(tuple(int,int,int), int) | map of core x,y,p to DataSpec region size |
RemoteSpinnakerUrl | str | url of the hpb machine | [C]
ResetMachineOnStartupFlag | bool | indicates if machine need to be restarted | [C] |
RouterCompressorProvenanceItems | list(ProvenanceDataItem) | provenance from a route compressor |
RouterProvenanceItems |  list(ProvenanceDataItem) | provenance from a router |
RoutingInfos | PartitionRoutingInfo | partition to its (keys and masks). | [M][I]
RoutingTableByPartition | MulticastRoutingTableByPartition | Routing infos mapped to partitions | [M]
RoutingTables | MulticastRoutingTable | routing tables | [M]
RunTime | float| runtime as requested by the user |
RunUntilCompleteFlag | bool | indatces cores should run as long as they think needed 
RunUntilTimeSteps | int | timestep to run to | [I]
ScampConnectionData | str | How to connect to scamp | [C][D]
SpallocServer| str | url to the spalloc server | [C] |
SystemMulticastRouterTimeoutKeys | dict(tuple(int,int),int) | core(x,y,p) tp broadcast router timeout keys | [I]
Tags | Tags | IP tags and reverse IP tags by Vertex| [M][I]
TotalRunTime | float | runtime possibly rounded up |
Transceiver |Transceiver | Object which talks to the baords | [m][I]
UnCompressedSummary | RouterSummary | Details written in the router Summary report  | [O]
VertexToEthernetConnectedChipMapping | dict(tuple(int,int),DataSpeedUpPacketGatherMachineVertex) |maps Ethernet cores to extra monitors | [M]
VirtualMachine |  Machine | A machine known to be virtual | [M]
WarnMessages | |list(str) | Warnings from the Chip Io Buffer Extractor | [O]

[C] Could come from the configs but also from other algorithms| ASB

[D] This value always appears to have the default so may be removed

[I] Also used with @inject_items

[M] In version 6.0.0 and earlier the name of many `<param_type>` started with Memory

[O] Provided as an algorithm output but never used anywhere


# BEYOND THIS POINT THIS DOCUEMENT IS OUT OF DATE!

# <a name="Algorithms"></a> Algorithms currently supplied

## Algorithms in the simplest run

| Algorithm | Use | Output
|:---------|:--------|
MachineGenerator | Reads description of the Machine of the boards | Machine, Transceiver
MallocBasedChipIDAllocator | Assigns virtual chips to Virtual vertices | ExtendedMachine
SpynnakerSplitterSelector | Make sure every vertex has a spliiter | token SplitterObjectsAllocated.MAIN
DelaySupportAdder | Adds any required delay vertices | token SplitterObjectsAllocated.DELAYS
SpYNNakerSplitterPartitioner | Creates a graph where each node runs on 1 core | MachineGraph NChipsRequired token PartitioningDone
EdgeToNKeysMapper | Works out the number of keys needed for each edge | MachinePartitionNKeysMap
LocalTDMABuilder | Configure Time Division Multiple Access | NONE!
SpreaderPlacer | works out which vertex to run on which core
2021-07-12 13:19:28 INFO: Time 0:00:00.000260 taken by NerRouteTrafficAware
2021-07-12 13:19:28 INFO: Time 0:00:00.000470 taken by BasicTagAllocator
2021-07-12 13:19:28 INFO: Time 0:00:00.000188 taken by ProcessPartitionConstraints
2021-07-12 13:19:28 INFO: Time 0:00:00.000362 taken by ZonedRoutingInfoAllocator
2021-07-12 13:19:28 INFO: Time 0:00:00.000262 taken by BasicRoutingTableGenerator
2021-07-12 13:19:28 INFO: Time 0:00:00.000197 taken by LocateExecutableStartType
2021-07-12 13:19:28 INFO: Time 0:00:00.001619 taken by BufferManagerCreator
2021-07-12 13:19:28 INFO: Time 0:00:00.000182 taken by SDRAMOutgoingPartitionAllocator
2021-07-12 13:19:28 INFO: Time 0:00:00.005974 taken by SpynnakerDataSpecificationWriter
2021-07-12 13:19:28 INFO: Time 0:00:00.002988 taken by RoutingSetup
2021-07-12 13:19:28 INFO: Time 0:00:00.000305 taken by GraphBinaryGatherer
2021-07-12 13:19:32 INFO: Time 0:00:03.689731 taken by PairOnChipRouterCompression
2021-07-12 13:19:32 INFO: Time 0:00:00.000675 taken by HostExecuteSystemDataSpecification
2021-07-12 13:19:32 INFO: Time 0:00:00.000861 taken by LoadSystemExecutableImages
2021-07-12 13:19:32 INFO: Time 0:00:00.003949 taken by TagsLoader
2021-07-12 13:19:32 INFO: Time 0:00:00.014179 taken by HostExecuteApplicationDataSpecification
2021-07-12 13:19:33 INFO: Time 0:00:00.513023 taken by SynapseExpander
2021-07-12 13:19:36 INFO: Time 0:00:03.404279 taken by OnChipBitFieldGenerator
2021-07-12 13:19:36 INFO: Time 0:00:00.000718 taken by FinishConnectionHolders
2021-07-12 13:19:44 INFO: Time 0:00:07.881266 taken by LoadApplicationExecutableImages
2021-07-12 13:19:44 INFO: Time 0:00:00.022663 taken by ChipRuntimeUpdater
2021-07-12 13:19:47 INFO: Time 0:00:02.742177 taken by DatabaseInterface
2021-07-12 13:19:47 INFO: Time 0:00:00.000640 taken by CreateNotificationProtocol
2021-07-12 13:19:47 INFO: Time 0:00:00.173868 taken by ApplicationRunner
2021-07-12 13:19:47 INFO: Time 0:00:00.006679 taken by BufferExtractor

## Deprecated Algorithm Names
| Original | Current |
|:---------|:--------|
MachineBitFieldUnorderedRouterCompressor | MachineBitFieldOrderedCoveringCompressor |
MundyOnChipRouterCompression | OrderedCoveringOnChipRouterCompression |
MundyRouterCompressor | OrderedCoveringRouterCompressor
SpynnakerMachineBitFieldUnorderedRouterCompressor | SpynnakerMachineBitFieldOrderedCoveringCompressor
UnorderedOnChipRouterCompression | OrderedCoveringOnChipRouterCompression

'ApplicationFinisher', 'ApplicationRunner', 'BasicDijkstraRouting', 'BasicRouteMerger', 
'BasicRoutingInfoAllocator', 'BasicRoutingTableGenerator', 'BasicSplitterSelector', 
'BasicTagAllocator', 'BitFieldCompressorReport', 'BoardChipReport', 'BufferExtractor', 
'BufferManagerCreator', 'ChipIOBufClearer', 'ChipIOBufExtractor', 'ChipProvenanceUpdater', 
'ChipRuntimeUpdater', 'CompressedRouterSummaryReport', 'ComputeEnergyUsed', 
'ConnectiveBasedPlacer', 'CreateNotificationProtocol', 'DSGRegionReloader', 'DatabaseInterface', 
'DelaySupportAdder', 'EdgeToNKeysMapper', 'EnergyProvenanceReporter',
'FinaliseTimingData', 'FindApplicationChipsUsed', 'FinishConnectionHolders', 
'FixedRouteFromMachineReport', 'FixedRouteRouter', 'GlobalZonedRoutingInfoAllocator', 
'GraphBinaryGatherer', 'GraphDataSpecificationWriter', 'GraphEdgeWeightUpdater', 
'GraphMeasurer', 'GraphProvenanceGatherer', 'HBPAllocator', 'HBPMaxMachineGenerator', 
'HostBasedBitFieldRouterCompressor', 'HostExecuteApplicationDataSpecification', 
'HostExecuteSystemDataSpecification', 'InsertChipPowerMonitorsToGraphs', 
'InsertEdgesToExtraMonitorFunctionality', 'InsertEdgesToLivePacketGatherers', 
'InsertExtraMonitorVerticesToGraphs', 'InsertLivePacketGatherersToGraphs', 'KeyConstraintAdder', 
'LoadApplicationExecutableImages', 'LoadFixedRoutes', 'LoadSystemExecutableImages', 'LocalTDMABuilder', 
'LocateExecutableStartType', 'MachineBitFieldOrderedCoveringCompressor', 'MachineBitFieldPairRouterCompressor', 
'MachineGenerator', 'MallocBasedChipIDAllocator', 
'MallocBasedRouteMerger', 'MallocBasedRoutingInfoAllocator', 'MemoryMapOnHostChipReport', 
'MemoryMapOnHostReport', 'NerRoute', 'NerRouteTrafficAware', 
'NetworkSpecificationReport', 'OnChipBitFieldGenerator', 'OneToOnePlacer', 'OrderedCoveringCompressor', 
'OrderedCoveringOnChipRouterCompression', 'PairCompressor', 'PairOnChipRouterCompression', 
'PairUnorderedCompressor', 'PartitionerReport', 'PlacementsProvenanceGatherer', 
'PlacerReportWithApplicationGraph', 'PlacerReportWithoutApplicationGraph', 
'PreAllocateForBitFieldRouterCompressor', 'PreAllocateResourcesForChipPowerMonitor', 
'PreAllocateResourcesForExtraMonitorSupport', 'PreAllocateResourcesForLivePacketGatherers', 
'ProcessPartitionConstraints', 'ProfileDataGatherer', 'ProvenanceJSONWriter', 'ProvenanceSQLWriter', 
'ProvenanceXMLWriter', 'RadialPlacer', 'ReadRoutingTablesFromMachine', 'RedundantPacketCountReport',
'RouterCollisionPotentialReport', 'RouterProvenanceGatherer', 'RouterReports', 'RouterSummaryReport',
'RoutingCompressionChecker', 'RoutingSetup', 'RoutingTableFromMachineReport', 'RoutingTableLoader',
'SDRAMOutgoingPartitionAllocator', 'SdramUsageReportPerChip',
'SpYNNakerConnectionHolderGenerator', 'SpYNNakerNeuronGraphNetworkSpecificationReport',
'SpYNNakerSplitterPartitioner', 'SpallocAllocator', 'SpallocMaxMachineGenerator', 
'SplitterPartitioner', 'SplitterReset', 'SpreaderPlacer', 'SpynnakerDataSpecificationWriter', 
'SpynnakerMachineBitFieldOrderedCoveringCompressor', 'SpynnakerMachineBitFieldPairRouterCompressor', 
'SpynnakerSplitterSelector', 'SynapseExpander', 
'SynapticMatrixReport', 'SystemMulticastRoutingGenerator', 'TagReport', 'TagsFromMachineReport', 'TagsLoader',
'ValidRoutesChecker', 'VirtualMachineGenerator', 'WriteJsonMachine', 
'WriteJsonMachineGraph', 'WriteJsonPartitionNKeysMap', 'WriteJsonPlacements', 'WriteJsonRoutingTables', 
'ZonedRoutingInfoAllocator', 'comparisonOfRoutingTablesReport', 'compressedRoutingTableReports', 
'routingInfoReports', 'unCompressedRoutingTableReports']



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
