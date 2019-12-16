---
title: Converting code to time based
layout: default
---

# Time based rather than timestep based

To allow for vertextes to run at different timestep the whole system is being changed to time based.

This requires many minor changes nearly everywhere.

The main system will however guarantee that the time invetervals used are a multiple of the vertextes timestep.

# SDRAM
Now time based rather than timestep based
1. get_total_sdram(self, n_timesteps)  removed
2. get_sdram_for_simtime(self, time_in_us) added
- Will however raise an Exception is time_in_us is not an exact multiple of timestep_in_us
3. Automatic handling of different timestep_in_us values

## VariableSDRAM
1. Takes an extra timestep_in_us paramater
2. per_timestep_sdram Only needs to be correct (or over) for time increments that are a multiple of per_timestep_sdram

## TimeBasedSDRAM
For vertexes with Variable time based on something other than timesteps
1. Must be accurate (or over) for any time_in_us
2. Automatically combinable with VariableSDRAM

# ResourceTracker
1.  minimum_simtime_in_us replaces plan_n_timesteps
2. Automatically handles everything simtime based

# Vertexes

## All Vertexes

Changes to AbstractVertex which effect all vertexes

1. timestep_in_us
- AbtractProperty that must be implemented
2. simtime_in_us_to_timesteps
- Utils method that converts simtime_in_us to timesteps
- Returns the exact number of timesteps as an int
- Uses timestep_in_us property
- Raises an exception if simtime is not an exact multiple

## ApplicationVertex
1. Must provide a timestep_in_us
- Suggested implementation
* Add a _timestep_in_us variable
* return _timestep_in_us as timestep_in_us
* add timestep_in_us to init with a None default.
If none call globals_variables.get_simulator().user_time_step_in_us  (unittest with 1000)
2. create_machine_vertex
To the MachineVertex init add a param timestep_in_us=self.timestep_in_us


## MachineVertex
1. Extra timestep_in_us param in the constuctor
- Will be saved an returned as property with the same name
2. ALL SubClasses myst pass timestep_in_us down
3. test Vertexes may use 1000 as the timestep_in_us

### AbstractGeneratesDataSpecification
1. Removed machine_time_step from generate_data_specification and generate_machine_data_specification


## Moves
ApplicationFPGAVertex and ApplicationSpiNNakerLinkVertex moved to  spinn_front_end_common/abstract_models/
1. This to allow then to access global variables

# Algorithms

## Params Changed
1. MachineTimeStep  Removed
- Ideally get timestep from the Vertexes
- UniqueTimeSte added for cases that the timestep can not come from Vertexes. Will be None for graphs with multiple timesteps
2. PlanNTimeSteps -> MinimumSimtimeInUs
- Unit changed from timestep to microseconds
3. DataNTimeSteps -> DataSimtimeInUs
- Unit changed from timestep to microseconds
4. RunTime -> RunTimeInUs
- Unit changed from milliseconds (float) to microseconds (int)
5. RunUntilTimeSteps -> RunUntilTimeInUs
- Unit changed from timestep to microseconds
6. FirstMachineTimeStep -> RunFromTimeInUs
- Unit changed from timestep to microseconds

## Changes required
1. Use new params
2. SDRAM.get_sdram_for_simtime
3. ResourceTracker with minimum_simtime_in_us


