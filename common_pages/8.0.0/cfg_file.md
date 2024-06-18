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


# Default values
For nearly all values the system comes with working default values 
so the best is to remove these in your cfg.  

The only required cfg settings are the ones related to accessing spinnaker.

# Specifying how to access spinnaker

1. Open either your `.spynnaker.cfg` (when using SpyNNaker) or `.spinnakerGraphFrontEnd.cfg` (when using the SpiNNakerGraphFrontEnd).
1. Modify the parameters within the `[Machine]` section.

## version
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

Where you edit spalloc_server if you are using a different spalloc_server; editing spalloc_user is helpful for administrators of the machine to contact you if there are any problems, which is why we suggest using an email address.

In this case spalloc_server is without the `http`/`https`.

### Spalloc Proxy Server

To use this option you must have an account setup by the spinnaker team.

```
[Machine]
version = 5
spalloc_server = https://user_id:password@spinnaker.cs.man.ac.uk/spalloc/
``````
Where 'user_id' and 'password' should be the ones setup and that workto log into the [server](pinnaker.cs.man.ac.uk/spalloc/).

To avoid exposing user_id and password in a clear text file 
set the evironment variables "SPALLOC_USER" and "SPALLOC_PASSWORD".   

### Local Board

Within the file, you should set `machineName` to the IP address or hostname of your SpiNNaker machine, and `version` to the version of your SpiNNaker board; this will almost certainly be "`3`" for a 4-chip board or "`5`" on a 48-chip board. The default IP address for a spinn-3 board is `192.168.240.253` and the default IP address for a spinn-5 board is `192.168.240.1`.

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


1. Open either your `.spynnaker.cfg` (when using SpyNNaker) or `.spinnakerGraphFrontEnd.cfg` (when using the SpiNNakerGraphFrontEnd).
1. Modify the parameters within the `[Machine]` section.
1. Modify "`virtual_board = False`" to state "`virtual_board = True`".
1. Modify/ Add "version = 5" to state you are simulating a spin1 48 chip board
   1. Use 3 to simulate a spin1 4 chip 
   1. Use 201  to simulate a spin2 single chip board
   1. Use 248 to simulate a spin2 48 chip board
1. Width and height of the virtual machine
   1. For versions 3 and 201 this is fixed and unchangable
   1. Like with Spalloc the system will calculate the number of board needed
      1. Use "`width = None`"
      1. Use "`height = None`"
   1. Optional (mainly to simulate a wrap around machine)
      1. Modify "`width = None`" to state the size of your virtual SpiNNaker machine in the _x_ dimension.
      1. Modify "`height = None`" to state the size of your virtual SpiNNaker machine in the _y_ dimension.
1. Advanced Machine settings
   1.`requires_wrap_arounds` No longer needed. A Width or Height which is a multiple of 12 causes wrap arround.

# Now what?

Run your scripts as normal, and either front end will generate a SpiNNaker machine with the dimensions you have defined and will execute all of its mapping processes as if it were running on a real machine.

When your script has reached the state where, when running on a real SpiNNaker machine, it would be loading data onto the SpiNNaker machine, it will now return immediately.  When used with PyNN scripts, you will be able to request data from the simulation, but this data will be empty.  When used with the Graph Front End, the results will depend on the user implementation.
