---
title: Affects of some on the Settings on how a Script runs
---
This page describes an older version. 
Please see [the latest version](latest/SettingEffects.html) or [home page](/) 

This page describes the settings that may change how a script is run, but in prinicple not what the script does.

It is currently under development so not all settings that change the way a script is run are listed.

# Contents
* [Config Settings](#config)
* [Script Setting](#script)
* [Recording](#recording)

# <a name="config"></a> Config Setting
## Location
The main places that config files are found is.

1. Within the code base
1. In the users home directory
1. The directory from which the script is run.
 
Remember that the configs use a last in rule so settings in a later file (for example the script directory) override the ones read in early (for example from the code base.)
   
The easiest way to find which config files a script is using is to run it and look for the Info: Read cfg files
These are listed in order the are read so the values in the later ones has presidence.

## Machine
Settings in the Machine section define where the scripts are run.
All scripts should run exactly the same on any type of machine with a few minor notes.
1. On a single or few board systems scripts can easily get to big to fit.
2. On Spalloc all known scripts fit but you will get different physical boards each run which may have minor effects on the placements.
 
### time_scale_factor
This adjusts how fast the code runs. The default when set to None is 1, which is real time.

Setting a higher value reduces the risk of timeover flows and increases the time the run phase takes.
It should have no other effect on your script.

### enable_advanced_monitor_support
When set to True (The default) it uses one of the cores on each chip to allow for faster data extraction.

As this uses up one core per chip larger script will fails to run on single boards sooner.

### max_sdram_allowed_per_chip
This should only be used when debugging algorithms and will always have a negetive effect if used.

## Reports
Each Extra report turned on may add an extra step to the full process of executing a script but most do not change how the script is run.

### extract_iobuf
These will effect how logging info is ready of the machione.

## Mode
See Reports which this effects.

## Simulation
TO DO

## Mapping
These settings should only been changed by people who are developing their own algorithms.

## Buffers
### use_auto_pause_and_resume
If set to true longer runs could be broken up into smaller sub runs to allow data to be extracted before the script runs.

This could result in more neurons/nodes on each core so that the code uses less chips/boards but means that longer runs are paused resulting in possibly longer overall execution times.
However it also means that scripts that would otherwise be impossible to run especialy on small systems will now work.
  
### minimum_auto_time_steps
This defines the minimum amount of time reach step in a chain of run pauses loops should be.

Setting this higher may require the paritionoer to split a population/node up more aggressively resulting in 
more cores being used or eventually even running out of available sdram resource.

Lowering this may allow more neurons/nodes on a single core allowing a script to fit on a single board that otherwise would not.

(Under development) This also guarantees that enough space is reserved on each core to run for at least that long even if the first run is shorter.
This may avoid the need to use auto pause resumes in subsequent calls to run which are shorter than the first call.
 
# Java
 
# <a name="script"></a> Script Setting
# <a name="recording"></a> Recording
