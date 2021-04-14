---
title: Executing the SpiNNaker software stack in "virtual mode"
---
# The version described here is no longer supported. 

[Home page for current version](/) 

This guide will detail how to operate either front end to the SpiNNaker software stack in "virtual mode". This results in the end user not needing a board to test basic operation of their script.

# Why Would you use Virtual mode?

1. Some people do not have either direct access to a SpiNNaker board or indirectly via the HBP portal, and therefore debugging their scripts within virtual mode can be useful.
1. People who have access to a SpiNNaker board remotely via the HBP portal may find it useful to operate in a virtual mode first to test their script for simple mistakes.

# How to make The software release operate in "virtual mode"?

1. Open either your .spynnaker.cfg (When Using SpyNNaker) or .spinnakerGraphFrontEnd.cfg (when using the SpiNNakerGraphFrontEnd). 
1. Modify the parameters within the [Machine] section.
1. Modify "width = None" to state the size of your virtual SpiNNaker machine in the x dimension. 
1. Modify "height = None" to state the size of your virtual SpiNNaker machine in the y dimension. 
1. Modify "virtual_board = False" to state "virtual_board = True".
1. If you wish to represent a virtual SpiNNaker machine which is wired as a toroid, please set "requires_wrap_arounds" from False to True

# Now what?

Run your scripts as normal, either front end will generate a SpiNNaker machine with the dimensions you have defined and will execute all of its mapping processes as if it was running on a real machine. 

When your script has reached the state where, when running on a real SpiNNaker machine, it would be loading data onto the SpiNNaker machine, it will now return immediately.  When used with PyNN scripts, you will be able to request data from the simulation, but this data will be empty.  When used with the Graph Front End, the results will depend on the user implementation.
