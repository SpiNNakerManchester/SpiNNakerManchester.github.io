---
title: The cfg file to control Spinnaker
---
This guide will detail how to configure either front end (sPyNNaker, or SpiNNakerGraphFrontEnd)

# Jupyter
For most users the easiest way to access Spinnaker is to use [Jupyter](https://spinnakermanchester.github.io/latest/jupyter.html)

The cfg is automatically set for you there and is unlikely to need changing.

# The cfg file
Spinnaker is controlled by a cfg file.
1. `.spynnaker.cfg` when using SpyNNaker (including PyNN)
1. `.spinnakerGraphFrontEnd.cfg` when using the SpiNNakerGraphFrontEnd

This file will be found in your home directory.

Warning some systems consider these a hidden file.

In Jupyter this can be edited using nano ~/.spynnaker

## Creating a new cfg file
When SpyNNaker is first called, if a configuration file is not found, it will create one in your home directory and exit.
It is possible to ask spinnaker to do this before you run your first simulation as follows:

### SpyNNaker

    import pyNN.spiNNaker as sim
    sim.setup()
    sim.end()

### SpiNNakerGraphFrontEnd

    import spinnaker_graph_front_end as front_end
    front_end.setup()
    front_end.end()

## Other cfg files.
Before reading the cfg in your home directory Spinnaker will load the default cfg files.

Any values in your cfg overwrites the default values.

Then it looks for a spynnaker.cfg/spinnakerGraphFrontEnd.cfg (No period) in the directory from which you run the script.
Values here overwrite the ones in your home cfg.
These are for values specific to the(se) script(s).

#  <a name="defaults"> Default values</a>
For all values the system comes with working default values.
So only include values where the default does not work for you. 

The only required cfg settings are the ones related to accessing spinnaker, as by default no access is defined.

The default values come from cfg files in each repository.
- [spinn_utilities.cfg](https://github.com/SpiNNakerManchester/SpiNNUtils/blob/master/spinn_utilities/spinn_utilities.cfg)
- [spinn_machine.cfg](https://github.com/SpiNNakerManchester/SpiNNMachine/blob/master/spinn_machine/spinn_machine.cfg)
- [spinnman.cfg](https://github.com/SpiNNakerManchester/SpiNNMan/blob/master/spinnman/spinnman.cfg)
- [pacman.cfg](https://github.com/SpiNNakerManchester/PACMAN/blob/master/pacman/pacman.cfg)
- [spinnaker.cfg](https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/blob/master/spinn_front_end_common/interface/spinnaker.cfg)
- [spynnaker.cfg](https://github.com/SpiNNakerManchester/sPyNNaker/blob/master/spynnaker/pyNN/spynnaker.cfg) / [spiNNakerGraphFrontEnd.cfg](https://github.com/SpiNNakerManchester/SpiNNakerGraphFrontEnd/blob/master/spinnaker_graph_front_end/spiNNakerGraphFrontEnd.cfg)

All cfg values used by the Spinnaker system are in these files.
The option names are case-insensitive and slashes are removed.
Do not edit these files. Instead, add the values you want to change to the cfg file in your home or run directory.

# Specifying how to access spinnaker

1. Open either your `.spynnaker.cfg` (when using SpyNNaker) or `.spinnakerGraphFrontEnd.cfg` (when using the SpiNNakerGraphFrontEnd).
1. Modify the parameters within the `[Machine]` section.

## Version
The system needs to know what version/type of board(s) is being used and how to access it.

Modify/ Add 'version' to one of these values
   - `3`: For a spin1 4 chip 
   - `5`: For a spin1 48 chip board
   - `201`:  For a spin2 single chip board
   - `248`: For a spin2 48 chip board

## Access method.

You use exactly one of the following making sure the other values are noe or better yet removed/commented out.

### Spalloc Classic Server

Due to local IP address of the boards this only works if physically inside the Manchester University network.

```
[Machine]
version = 5
spalloc_server = spinnaker.cs.man.ac.uk
spalloc_user = user.name@email.address
```

In this case spalloc_server is without the `http`/`https`.

On https://spinn-20.cs.man.ac.uk/ (Our JupyterLab)
```
[Machine]
version = 5
spalloc_server = 10.11.192.11
spalloc_user=Jupyter(your id)
```

Where you edit spalloc_server if you are using a different spalloc_server; 
Editing spalloc_user is helpful for administrators of the machine to contact you if there are any problems, which is why we suggest using an email address.


### Spalloc Proxy Server

To use this option you must have an account setup by the spinnaker team.

```
[Machine]
version = 5
spalloc_server = https://user_id:password@spinnaker.cs.man.ac.uk/spalloc/
``````
Where 'user_id' and 'password' should be the ones setup and that work to log into the [server](spinnaker.cs.man.ac.uk/spalloc/).

To avoid exposing user_id and password in a clear text file 
set the evironment variables "SPALLOC_USER" and "SPALLOC_PASSWORD".   

### Local Board

Within the file, you should set `machineName` to the IP address or hostname of your SpiNNaker machine, and `version` to the version of your SpiNNaker board; this will almost certainly be "`3`" for a 4-chip board or "`5`" on a 48-chip board.
The default IP address for a spinn-3 board is `192.168.240.253` and the default IP address for a spinn-5 board is `192.168.240.1`.

```
[Machine]
version = 3
machineName = 192.168.240.253
``````

Go to the network settings for your computer and add or set an IPv4 entry with the following address for the adapter connected to the SpiNNaker board:

 1. IP address = `192.168.240.254`
 2. sub-mask = `255.255.255.0`
 3. default gateway = `0.0.0.0`

### Virtual Board

#### Why would you use "virtual mode"?

1. Some people do not have either direct access to a SpiNNaker board or have indirect access via the HBP portal, and therefore debugging their scripts within virtual mode can be useful.
1. People who have access to a SpiNNaker board remotely via the HBP portal may find it useful to operate in virtual mode first to test their script for simple mistakes.

#### Previous versions
[For versions upto and including 7.1.0](.common_pages/6.0.0/VirtualMode.html)

#### How to make the software release operate in "virtual mode"

To use a virtual board pick the version you want to simulate and set virtual_board to True.

```
[Machine]
version = x
virtual_board = True
``````

Optional (mainly to simulate a wrap around machine)
   1. Modify "`width = None`" to state the size of your virtual SpiNNaker machine in the _x_ dimension.
   1. Modify "`height = None`" to state the size of your virtual SpiNNaker machine in the _y_ dimension.

For example: To simulate a three board wrapped setup.
```
[Machine]
version = 5
virtual_board = True
width = 12
height = 12
``````

# <a name="mode">Mode</a>
The cfg files include a lot of flags to say which reports should be run, what data to extract and what to delete at the end of a run.

To make it easier to turn these on the cfg includes an option

````
[Mode]
mode=Production
````

Mode supports 4 values Production, Info, Debug, All

These working by changing the values of some individual cfg settings.
(Note this is done after reading all cfg files so where the mode and indiviaul settings are define is irrelevant here)

The individual csf settings can start with four values True, Info, Debug and False.
These are then converted to True or False depending on the mode.

- Production: Info and Debug converted to False
- Info: Info converted to True and Debug to False
- Debug: Info and Debug are converted to True
- All: All processed cfg settings changed to True

By defualt none of the cfg settings are True and only a small subset are Info.
All the rest except those that change the placements or compression are Debug.
The ones False by default are:
- write_energy_report: Adds Engery monitor vertices so changes what is placed where
- router_table_compress_as_far_as_possible: Causes the compressor to run longer than needed, Does not improve run preformance.

## Seeing the cfg settings
There are three ways tio disciver what all the changable cfg settings are:
- Mode=Debug: There will be logs of all the cfg flags changed
- skipped as logs: Whenever something is not done there is a log message like Extract IO buff skipped as cfg Reports:extract_iobuf is False
  (Note this is False after the changes made by mode)
- Looking at the [default](#defaults) cfg files

## Prior to version 7.3.0 
There were only two 
- Production (acted like the current Info)
- Debug (acted like the current All)

cfg Flags can only be True or false
