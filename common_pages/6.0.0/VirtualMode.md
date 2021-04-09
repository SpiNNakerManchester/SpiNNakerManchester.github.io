---
title: Executing the SpiNNaker software stack in "virtual mode"
---

This guide will detail how to operate either front end (sPyNNaker, or SpiNNakerGraphFrontEnd) to the SpiNNaker software stack in "virtual mode". This results in the end user not needing a board to test the basic operation of their script.

# Why would you use "virtual mode"?

1. Some people do not have either direct access to a SpiNNaker board or have indirect access via the HBP portal, and therefore debugging their scripts within virtual mode can be useful.
1. People who have access to a SpiNNaker board remotely via the HBP portal may find it useful to operate in virtual mode first to test their script for simple mistakes.

# How to make the software release operate in "virtual mode"

1. Open either your `.spynnaker.cfg` (when using SpyNNaker) or `.spinnakerGraphFrontEnd.cfg` (when using the SpiNNakerGraphFrontEnd).
1. Modify the parameters within the `[Machine]` section.
1. Modify "`width = None`" to state the size of your virtual SpiNNaker machine in the _x_ dimension.
1. Modify "`height = None`" to state the size of your virtual SpiNNaker machine in the _y_ dimension.
1. Modify "`virtual_board = False`" to state "`virtual_board = True`".
1. If you wish to represent a virtual SpiNNaker machine which is wired as a toroid, please set "`requires_wrap_arounds`" from False to True

# Now what?

Run your scripts as normal, and either front end will generate a SpiNNaker machine with the dimensions you have defined and will execute all of its mapping processes as if it were running on a real machine.

When your script has reached the state where, when running on a real SpiNNaker machine, it would be loading data onto the SpiNNaker machine, it will now return immediately.  When used with PyNN scripts, you will be able to request data from the simulation, but this data will be empty.  When used with the Graph Front End, the results will depend on the user implementation.
