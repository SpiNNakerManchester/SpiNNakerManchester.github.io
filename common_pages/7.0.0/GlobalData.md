---
title: Using Global Data
layout: default
---
The way that much of the data used by the simulator changed in July 2022.

This reduced the number of parameters passed through methods.

Background
==========
In the past data objects were indirectly held by the simulator and passed into
algorithms based on the xml files.
From the algorithms this data was then often passed through a whole series of method calls.
Some additional data was injected into methods as needed based on customised injector code.

This often made it very hard to track where the data originally came from
and where it was actually used.
It also made it hard to know if the various copies of the data were all
pointers to the same instance or multiple copies.
There was also the worry that if data was exposed it could be manipulated in
unsupported ways leading to errors that were hard to debug.

There was a time between releases 6.0 and 7.0 where the data was held by AbstractSpinnakerBase
(ASB) and passed directly into the algorithm but that version is no longer supported.

Quick Usage
=====
To access any global data just call the appropriate DataView class method.

For example to access the Transceiver do:
~~~
SpynnakerDataView.get_transceiver()
~~~
or for GraphFrontEnd users do:
~~~
FecDataView.get_transceiver()
~~~

Do not cache the data; rather, repeat the View call each time so that you always
have access to the current data even if a new data object is created.

Do not change any data received from the View in any way,
other than using one of the View's add methods.
New data should be passed back to the simulator which should then add it.

Model
=====

The global data is now held by a series of DataModel classes that are designed
to be singletons so that only a single copy of each data item exists at a time.
These classes should not be accessed directly.
There are also a number of status enums which are designed for internal
(within Views) usage only.

The data is accessible through the DataView classes which provide all the
required class methods for accessing the data on demand.
There is a DataView at each code repository level with each level inheriting all the
method from previous levels.
GraphFrontEnd Users should therefore always use FecDataView, while PyNN users should use SpynnakerDataView.

There are also a series of DataWriter classes.
These are designed so there can is only ever one Writer Object at a time as
creating a new Writer Object will clear all the data in the model.
The only place Writer Objects should be created is in ASB or in unit tests.

Generally (except in unittests) data is added to the model by returning the value to ASB which then adds it.
Where it is reasonable for users or algorithm to add data directly the Views will have methods for doing so.
These View methods may include safety code to prevent unexpected changes.

The View Methods
================
The first word in a View method gives an indication of how the method reacts.
The remaining words say on what data the method acts.

The best and most up to date place for details of each method is its code docs.

check...
-------
check... methods are designed for safety code.

They will raise an exception in an unexpected situation.
Otherwise they do nothing and return nothing.

For example check_user_can_act() checks that the call is between sim.setup and sim.end,
and not during the processing of sim.run or sim.stop.

get...
---
get methods do as they say and get/return some kind of data.

As a reasonable attempt is made to validate the data,
a get method should be trusted to return the type of data documented.
(If by some chance a get method is found to return the wrong data
the correct fix is to improve the validation in the Writer class)

Unless specifically documented to do so the get methods will not return None.
Instead they will raise an Exception that the data is not available.
Where code needs to know if data is available a "has" methods has been or should be added.

Some get methods will create a mocked value if called while in unittest mode.
These should be documented as such.
For example the path methods like get_run_dir_path() return a temp dir and
get_machine returns a virtual machine.
Unittests should not count on a specific Object being returned
but only on the Type of Object being returned.

As well direct access to data objects there are also semantic sugar get methods.
These will typically be where the same pattern of View.getFoo().bar was used in several places.
Sometimes the behaviour of the semantic sugar method may be different for edge case.
These should be documented in the code docs.
A few semantic sugar methods not starting with get are listed in the semantic sugar section.

For example get_chip_at() is like machine.get_chip_at(x, y),
except that instead of returning a None it raises an Exception if x, y are invalid.

add...
---
These methods are for adding additional data.

While the normal way to add data is for the Algorithm to return data to the simulator
there are times when it makes sense not to pass through the simulator.
For example to avoid the need to expose the ASB just so a call could be made add data.

They typically include safety code that can not be called at an unexpected time.
For example the add_vertex method will raise an Exception if called during run.

has...
---
The has methods return True if the corresponding get method would
return a value rather than raise an Exception.

If the get method would mock a value in unittest mode,
the has method returns True in unittest mode even if the underlying Object has not yet been created.

For example has_machine() returns True if there is a machine Object saved
but will also return True while testing as it knows it can create a Virtual Machine if requested to do so.

has_time_step

In theory every get method could have a matching has method.
In practice has methods have only been created where there is a current need for them.
Rather than wrap a get method in a try consider adding a has method.

is...
--
The is methods are used to access the current status of the simulator.

For example is_ran_last() reports if this is a second or later run without a reset.

is... methods should always return a bool value.

is... methods may raise an Exception if called at a time where the question does not make sense.
For example is_ran_last() raises an Exception if called before sim.setup

iterate...
------
These methods provide a way of iterating over the data.

Their main purpose is to protect a data object that is changed over time by only exposing their data through iterators.

where_is...
--------
These are debugging/logging methods that will always return s string description as best they can,
even if that String is just the Exception message.

semantic_sugar
--------------
To keep the name the same as before these methods don't follow the normal naming pattern

free_id for transceiver.app_id_tracker.free_id

read_memory for transceiver.read_memory

write_memory for transceiver.read_memory

register_binary_search_path for executable_finder.add_path


underscore methods
------------------
These are for internal (within Views and Writers only).

If they are needed elsewhere they should be converted to normal methods.

Data Renamed
============
(OriginalApplication/Machine)Graph
----------------------------------
As long term plans in other branches are to remove cloned graphs used during runtime,
the methods that access the "Original" or user graphs no longer have the word Original in the name.

As long term plans in other branches are to remove the MachineGraph,
the methods that access the Application graph no longer have the term "Application".

These graph objects are not directly accessible. Instead use the iterate and get methods to
access the graph's data and the add method to change the graph.

Application/MachineGraph
------------------------
The cloned graphs that the Algorithms accessed are temporarily available through
get_runtime_graph and get_runtime_machine_graph.
As well as get_runtime_best_graph for methods that need a graph but don't mind which one.

These graphs remain directly accessible due to the long term plans to remove them,
which would then mean the removal of these methods.

In the unlikely case that the work to remove the cloned graphs does not make it in,
we reserve the right to replace the get_runtime_(machine)_graph methods with iterators and add methods.

machine_time_step
-----------------
machine_time_step has been renamed simulation_time_step to highlight that it
is the rate that the simulation mathematically thinks it is running at.

The hardware_time_step is the clocktime taken by the hardware to compute each timestep.
If the time_scale_factor is not 1 these two times will differ.

run_until_timesteps/ RunUntilTimeSteps
--------------------------------------
The number of timesteps a run should or has run for had many different names.
The data is now available as ...View.get_current_run_timesteps()

current_time
------------
Now available as ...View.get_current_run_time... to show it is the runtime and not clocktime and to highlight the units

data_n_time_steps/DataNTimeSteps
--------------------------------
data_n_time_steps is now available as View.get_max_run_time_steps()
This better reflects that the value says the maximum timesteps a run could be before auto pause and resume kicks in.
This is mainly used to size recording regions.

ExtendedMachine
---------------
As ASB now controls when algorithms are run the distinction between machine and extended machine has been dropped.

n_chips_required
----------------
n_chips_required is now only the value provided by the user during setup so is not a global data item.
Instead n_chips_needed is supplied which will be either the user supplied value or if not supplied the one calculated by the partitioner.

(app/system)_provenance_file_path
---------------------------------
(app/system)_provenance_file_paths have been renamed get_(app/system)_provenance_dir_path as it is actually a directory.

run_report_directory / default_report_directory/report_default_directory()
--------------------------------------------------------------------------
The run_report_directory is now exposed by get_run_dir_path().

This points to the run_X directory under the timestamped directory.

Renamed to avoid the confusion that this could be the "reports" directory which hold all the runs over time.


Inject_items
============
This has been completely removed.

View get methods exist for all items previously injected:

ApplicationGraph -> ...View.get_runtime_graph()
APPID -> ...View.get_app_id()
DataInMulticastKeyToChipMap -> ...View.get_data_in_multicast_key_to_chip_map()
DataNTimeSteps -> ...View.get_max_run_time_steps()
ExtendedMachine -> ...View.get_machine()
FirstMachineTimeStep -> ...View.get_first_machine_time_step()
MachineGraph -> ...View.get_runtime_machine_graph()
RoutingInfos -> ...View.get_routing_infos()
RunUntilTimeSteps -> ...View.get_current_run_timesteps()
SystemMulticastRouterTimeoutKeys -> ...View.get_system_multicast_router_timeout_keys()
Tags -> View.get_tags()

Why is View data sent as a parameter in some cases?
===================================================
There are two reasons why there are still cases where data is obtained from a View and then passed as a parameter.

Method not always using the View Data
------------------------------------
There are some cases where the same method or class is used both for the data as held in the View and
sometimes for different data or a reduced set of this data.

For example IOBufExtractor normally reads all the data
but in some cases for example in emergency_recover only recovers for some executable_targets.

The ideal in these cases is that if the data from the View could be used,
the param defaults to None, and if None, reads from the View.
That way only places that want non-View data need to worry about that data.

The Transceiver methods mainly still require an app_id.
This is partly because in some cases like get_multicast_routes a non-app_id already has the meaning anyway,
so could not mean the default.

Method not yet converted
-------------------------
There are still many cases, especially for local methods, that data obtained from a View is passed through.

This is because the conversion to using a View has not yet been done.

Sometimes this was to avoid clashes with other major rework and sometime just because the original PR was already so big.

There is no reason why over time these will not also be converted to using Views rather than Parameters.

Why is View data held in self._
-------------------------------
Holding of cacheed copies of View data is NOT RECOMMENDED.

The reason this is sometimes still done is the same as above.

Changed APIs
====================

AbstractAcceptsIncomingSynapses
-------------------------------
get_connections_from_machine
- transceiver removed
    - HasSynapses.get_connections_from_machine no longer needs a transceiver
- placements removed
    - use View.get_placement_of_vertex

AbstractEventRecordable
-----------------------
clear_event_recording
get_events
- buffer_manager removed
  - use ...View.get_buffer_manager()
- placements removed
  - use ...View.get_placement_of_vertex

AbstractGeneratesDataSpecification
----------------------------------
generate_data_specification
- @inject_items no longer works/needed

AbstractHasProfileData
----------------------
get_profile_data
- remove txrx
- get_profiling_data no longer needs a txrx passed in

AbstractNeuronRecordable
------------------------
clear_recording
- buffer_manager removed
  - use ...View.get_buffer_manager()
- placements removed
  - use ...View.get_placement_of_vertex

get_data
- n_machine_time_steps removed
    View.get_current_run_timesteps() when needed
- buffer_manager removed
  - use ...View.get_buffer_manager()
- placements removed
  - use ...View.get_placement_of_vertex

AbstractProvidesProvenanceDataFromMachine
-------------------------------------
get_provenance_data_from_machine
- txrx removed
    - use ...View.get_transceiver()

AbstractReadParametersBeforeSet
-------------------------------
read_parameters_from_machine
- transceiver removed
  - locate_memory_region_for_placement no longer needs a transceiver passed in

AbstractReceiveBuffersToHost
----------------------------
get_recording_region_base_address
- remove txrx
  - locate_memory_region_for_placement no longer needs a txrx passed in

AbstractRewritesDataSpecification
---------------------------------
regenerate_data_specification
- @inject_items no longer works/ is needed

AbstractSpikeRecordable
-----------------------
clear_spike_recording
get_spikes
- same as AbstractNeuronRecordable

AbstractSupportsBitFieldGeneration
----------------------------------
bit_field_base_address
bit_field_builder_region
- transceiver removed
  - locate_memory_region_for_placement no longer needs a transceiver passed in

AbstractSupportsBitFieldRoutingCompression
------------------------------------------
regeneratable_sdram_blocks_and_sizes
- transceiver removed
  - locate_memory_region_for_placement no longer needs a transceiver passed in

AbstractSynapseExpandable
-------------------------
read_generated_connection_holders
- transceiver removed
 - locate_memory_region_for_placement no longer needs a transceiver passed in

HasSynapses
-----------
get_connections_from_machine
- transceiver removed
- placement param kept



Unit Testing
===========
One disadvantage of the Global Data approach that it does make unittests harder to write.

Instead of creating the required objects and passing them into a method,
the unittest now has to add the Objects for the method to then get them from a View.

The Writer will have set... methods used by ASB to set the data.

There are also a number of back (protected) _set methods.
These normally only work for a writer created using the mock() call.

The unittests of most View methods will show how to add data to the view.

...DataWriter.mock()
--------------------
Unittests can obtain a Writer object using the call ...DataWriter.mock().
This return a Writer Object which can then be used to add data to the View.
This Writer Object will be in the Mocked state so that all View set methods will work.
The Mock state also allows the View to use mock objects as listed below.

Critical!: Every time a new Writer object is created it clears all data in the View!
Therefore each unittest should only create one Writer.
This includes the one line ...DataWriter().set... calls.

unittest_setup() at the PACMAN level and above calls DataWriter.mock so that any test that calls unittest_setup()
is guaranteed to be in mock state with cleared data.
(This is an exception to the above only call mock once as no data is set between the two mock calls).

Directories
-----------
There is no need to create directories as the Views will automatically create a temp directory if asked for any.

Machine
-------
There is no need to create a Machine object unless the test needs a specific Machine.
The Mocked Machine is currently a Virtual 48 Chip, but this can change without notice.

MachinePartitionNKeysMap
------------------------
In the Mock State the View will default to an Empty Map.

Other code changes:
===================

Placements iter method removed
------------------------------
The iter method of Placements object was removed as it was never used.
It was also confusing as to what it actually iterated over.
If x,y,p are needed a core_location iterator could be added.


















