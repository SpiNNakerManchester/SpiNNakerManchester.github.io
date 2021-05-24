Name| Type| ASB| Input | Output | Injected | Comment |
:---|:----|:---|:------|:-------|:---------|:--------|
APPID | int | _app_id | yes | no | no |
AppProvenanceFilePath |globals_variables
AutoDetectBMPFlag| bool | "auto_detect_bmp" / False if virtual| yes | yes | no |  allocators
AverageCoresOnChip| float| no | no| yes |no | FindApplicationChipsUsed untested
BMPDetails | str| "bmp_names" / None if virtual | yes| yes | no |   allocators
BitFieldSummary | BitFieldSummary| no | no| yes | no | BitFieldCompressorReport tested
BoardVersion | int | "version" | yes | yes | no |  allocators
BootPortNum| int| "boot_connection_port_num" | yes| yes |no |  allocators
BufferManager| BufferManager| _buffer_manager | yes| yes |no |
CompressedSummary| RouterSummary| no | no| yes |no|CompressedRouterSummaryReport triggered via cfg
CompressionAsFarAsPos| n/a
CompressionTargetSize| n/a
CompressorExecutableTargetsUsed| ExecutableTargets| no | no| yes |no | 3 algorithms
ConnectionHolders|  dict(tuple(ProjectionApplicationEdge, SynapseInformation), ConnectionHolder| no | 1| 1 |no | 
CreateAtomToEventIdMapping| n/a
DSGTimeMs| float| _dsg_time | 1| 1 |no | FinaliseTimingData?
DataInMulticastKeyToChipMap| typdict(tuple(int,int),int)| no | no| out |yes | 
DataInMulticastRoutingTables| MulticastRoutingTables| no | no| yes |yes |
DataNSteps | int | _max_run_time_steps | no| out |yes | same as  DataNTimeSteps
DataNTimeSteps| int| _max_run_time_steps | yes| out |yes | 
DataSpecificationTargets| dict(tuple(int,int,int),str) | no | yes| yes |no | 
DatabaseFilePath| str| passed | 1| 1 |no | 
DatabaseInterface| DatabaseInterface| no | no| 1 |no | used for external device interaction including visulisers
DatabaseSocketAddresses|set(SocketAddress)| _database_socket_addresses | in| no |no |
DatabaseWaitOnConfirmationFlag| n/a
DisableAdvancedMonitorUsageForDataIn|n/a
DownedChipsDetails| set(IgnoreChip)| parsed "down_chips"| yes|no|no | 
DownedCoresDetails| set(IgnoreCore)| parsed "down_cores" | yes| no |no | 
DownedLinksDetails| set(IgnoreLink| parsed "down_links"| yes| no |no|  
EndUserConfigurableSafetyFactorForTDMAAgenda| float| no | yes| no |no | https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/issues/788
ErrorMessages|list(str)| no | no| yes |no |
ExampleFilePath| n/a| n/a | n/a| n/a |n/a | Tests!
ExecutableFinder| ExecutableFinder| _executable_finder  | yes| no |no|
ExecutableTargets| ExecutableTargets| passed | yes| yes |no | 
ExecutableTypes| dict(ExecutableType,CoreSubsets or None)| to _executable_types | yes| yes |no | 
ExecuteTimeMs| float| no | 1| 1 |no | FinaliseTimingData?
ExtractIobufFromBinaryTypes| n/a
ExtractIobufFromCores| n/a
ExtractionTimeMs|float| no| 1| 1 |no | FinaliseTimingData?
FailedCoresSubsets| CoreSubsets| WEIRD | yes| no |no | https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/issues/784
FirstMachineTimeStep| int| _current_run_timesteps | yes| no |yes | Same as RunUntilTimeSteps?
FixedRouteDestinationClass| Class type| DataSpeedUpPacketGatherMachineVertex | 1| no |no | should this even be a param?
GenerateBitFieldReport| n/a
GenerateBitFieldSummaryReport| n/a
GraphProvenanceItems| list(ProvenanceDataItem)| used | no| yes |no |
IPAddress| str| _hostname | yes| yes |no |  allocators
IgnoreBadEthernets| n/a
JavaCaller|  JavaCaller|  JavaCaller(..) | yes| no |no |
JsonFolder| str (path)| _json_folder | yes| no |no |
JsonMachine| str (json)| no | no| yes |no | 
JsonMachineGraphPath| str (path)| no | no| yes |no |
JsonPartitionNKeysMap|str(path)| no | no| yes |no |
JsonPlacementsPath| str(path)| no | no| yes |no |
JsonRoutingTablesPath| str(path)|no| no| yes |no |
LivePacketRecorderParameters|  dict(LivePacketGatherParameters,
            list(tuple(AbstractVertex, list(str))))| _live_packet_recorder_params | yes| not |no |
LivePacketRecorderParametersToVertexMapping| dict(LivePacketGatherParameters,
            dict(tuple(int,int),LivePacketGatherMachineVertex))| no | 1| 1 |no |
LoadTimeMs|float| no | 1| 1 |no | FinaliseTimingData?
MCGathererCoresToAllocate| int| no | yes(optional)| no |no | Never set!
MachineAllocationController| MachineAllocationController| to _machine_allocation_controller  | yes| yes |no |  allocators
MachineHeight| n/a
MachineJsonPath| n/a
MachineTimeStep| global_variables
MachineWidth| n/a
MappingTimeMs| float| passed | 1| 1 |No | FinaliseTimingData?
MaxCoresUsedOnChip| int| no | no| yes |no | FindApplicationChipsUsed untested
MaxMachineCoreReduction| int| "max_machine_core_reduction" | yes| no |no | Better to use Machine.set_max_cores_per_chip
MaxSDRAMSize| n/a
ApplicationGraph| ApplicationGraph| _application_graph | yes| no |yes | 
CompressedRoutingTables| MulticastRoutingTables| no | yes| yes |no | 
MemoryExtendedMachine| Machine (with virtual chips)| no | yes| yes |yes |
MemoryExtendedVirtualMachine| ?type| no | no| yes |no | VirtualMallocBasedChipIDAllocator DEAD?
MemoryExtraMonitorToChipMapping| dict(tuple(int,int),ExtraMonitorSupportMachineVertex)| param for _locate_receivers_from_projections | yes| yes |no |
MemoryExtraMonitorVertices| list(ExtraMonitorSupportMachineVertex)| used by methods| yes |yes |no | use MemoryExtraMonitorToChipMapping.items()?
MemoryFixedRoutes| dict(tuple(int,int),FixedRouteEntry| to _fixed_routes | yes| yes |no | Nuke asb.fixed_route?
MemoryIpTags| nuked
MemoryMCGatherVertexToEthernetConnectedChipMapping| dict(tuple(int,int),DataSpeedUpPacketGatherMachineVertex)| used in methods | yes| yest |no |
MemoryMachine| MachineGraph| to .machine |yes|yes|yes|
MemoryMachineEdgeNKeysMap| n/a| no| -| no |no | nuked CompressibleMallocBasedRoutingInfoAllocator / nuked DestinationBasedRoutingInfoAllocator
MemoryMachineGraph| MachineGraph| _machine_graph | yes| yes |yes |
MemoryMachinePartitionNKeysMap| DictBasedMachinePartitionNKeysMap| no | yes| yes |yes |
MemoryNumberSamplesPerRecordingEntry| n/a
MemoryPlacements| Placements| to _placements | yes|yes|yes |
MemoryPlacements2| nuked
MemoryPreAllocatedResources| PreAllocatedResourceContainer| PreAllocatedResourceContainer() | yes| yes |no |
MemoryReverseIpTags| nuked
MemoryReverseTags| nuked
MemoryRoutingInfos| PartitionRoutingInfo| no | yes| yes |yes |
MemoryRoutingTableByPartition| MulticastRoutingTableByPartition| no | in| out |no |
MemoryRoutingTables| MulticastRoutingTables| to _router_tables | yes | yes |je |
MemorySamplingFrequency| n/a
MemoryTags|Tags| to _tags | in| out |yes |
MemoryTransceiver| Transceiver| to _txrx | yes| yes |no |
MemoryVirtualMachine| Machine| asb | yes| yes |no |
MinCoresUsedOnChip| int| no | no| 1 |no | FindApplicationChipsUsed untested
NBoardsRequired| int| _n_boards_required | yes| no |no |
NChipsRequired| int| _n_chips_required | yes| yes |no |
NChipsUsed| int| no | no| 1 |no |  FindApplicationChipsUsed untested
NPacketsPerTimeWindow| int| no | yes| no |no | https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/issues/788
NSyncSteps| int| __timesteps(sync_time)| yes| no |no |
NoSyncChanges| int| _no_sync_changes | yes| yes |no |
NotificationInterface| NotificationProtocol| check to close | yes| yes |no |
NumberOfCPUCyclesUsedByThePacketReceiveCallback| int| no | yes| no |no | https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/issues/788
NumberOfCpuCyclesByOtherCallbacks| int| no | yes| no |no |https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/issues/788
PlacementsProvenanceItems| list(ProvenanceDataItem)| used | yes| yes |no |
PlanNTimeSteps| int| yes | yes| no |no |
PostSimulationOverrunBeforeError| int| conditional set from "post_simulation_overrun_before_error" | yes| no |no |
PowerProvenanceItems| list(ProvenanceDataItem)| used | no| yes |no |
PowerUsed| PowerUsed| checked | yes| yes |no |
ProcessorToAppDataBaseAddress| type| asb | in| out |je |
ProvenanceItems| type| asb | in| out |je |
RegionSizes| type| asb | in| out |je |
RemoteSpinnakerUrl| type| _remote_spinnaker_url/"remote_spinnaker_url" | yes| no |je |
RepairMachine| n/a
ReportFolder| global_variables
ReportWaitingLogsFlag| n/a
ResetMachineOnStartupFlag| bool| "reset_machine_on_startup" | yes| yes |no |  allocators
RouterBitfieldCompressionReport| n/a
RouterCompressorBitFieldPercentageThreshold| n/a
RouterCompressorBitFieldPreAllocSize| n/a
RouterCompressorBitFieldRetryCount| n/a
RouterCompressorBitFieldTargetLength| nuked
RouterCompressorBitFieldTimePerAttempt| n/a
RouterCompressorBitFieldUseCutOff| n/a 
RouterCompressorProvenanceItems| list(ProvenanceDataItem)| no | yes| yes |no |
RouterProvenanceItems| list(ProvenanceDataItem)| used | yes| yes |no |
RunTime| float| param | yes| no |no |
"RunTimeMachineTimeSteps" ??
"RunTimeSteps" ??
RunUntilCompleteFlag| bool| set | yes| no |no |
RunUntilTimeSteps| int| set | yes| no |no |
ScampConnectionData| str| "scamp_connections_data" | yes| yes |no |  allocators
SpallocMachine|n/a
SpallocPort| n/a
SpallocServer| str| _spalloc_server/ "spalloc_server" | in| no|no |
SpallocUser| n/a
SynapticExpanderReadIOBuf| bool| "write_expander_iobuf" | yes| no |no |
SystemMulticastRouterTimeoutKeys| dict(tuple(int,int),int)|no | no| yes|yes |
SystemProvenanceFilePath| global_variables
TDMAAgenda| nuked
TimeScaleFactor| global_variables
TotalRunTime| float| param | yes| no |no |
UnCompressedSummary| RouterSummary| no | no| yes |no |
UserCreateDatabaseFlag| n/a
UserDefinedMaxDelay| float | __max_delay | yes| no |no |
UsingAdvancedMonitorSupport| n/a
UsingReinjection| n/a
WarnMessages| list(str)| no | no| yes |no |
WriteBitFieldGeneratorIOBUF| n/a
WriteCompressorIobuf| n/a
WriteDataSpeedUpReportsFlag| n/a
WriteTextSpecsFlag| n/a

