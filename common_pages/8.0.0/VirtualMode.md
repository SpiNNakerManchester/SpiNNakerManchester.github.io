---
title: Executing the SpiNNaker software stack in "virtual mode"
---

This guide will detail how to operate either front end (sPyNNaker, or SpiNNakerGraphFrontEnd) to the SpiNNaker software stack in "virtual mode". This results in the end user not needing a board to test the basic operation of their script.

# Why would you use "virtual mode"?

1. Some people do not have either direct access to a SpiNNaker board or have indirect access via the HBP portal, and therefore debugging their scripts within virtual mode can be useful.
1. People who have access to a SpiNNaker board remotely via the HBP portal may find it useful to operate in virtual mode first to test their script for simple mistakes.

# Previous versions
[For versions upto and including 7.1.0](.common_pages/6.0.0/VirtualMode.html)


# How to make the software release operate in "virtual mode"

1. Open either your `.spynnaker.cfg` (when using SpyNNaker) or `.spinnakerGraphFrontEnd.cfg` (when using the SpiNNakerGraphFrontEnd).
1. Modify the parameters within the `[Machine]` section.
1. Modify "`virtual_board = False`" to state "`virtual_board = True`".
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
