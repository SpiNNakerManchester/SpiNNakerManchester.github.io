---
title: Executing the sPyNNaker software stack in "virtual mode"
---

This guide will detail how to operate the sPyNNaker front end in "virtual mode". This results in the end user not needing a board to test basic operation of their PyNN script.

# Why Would you use Virtual mode?

1. Some people do not have either direct access to a SpiNNaker board or indirectly via the HBP portal, and therefore debugging their PyNN scripts within virtual mode can be useful.
1. People who have access to a SpiNNaker board remotely via the HBP portal may find it useful to operate in a virtual mode first to test their PyNN script for simple mistakes.

# How to make sPyNNaker operate in "virtual mode"?

1. Enter your .spynnaker.cfg file
1. Modify the parameters within the [Machine] section.
1. Modify "width = None" to state the size of your virtual SpiNNaker machine in the x dimension. 
1. Modify "height = None" to state the size of your virtual SpiNNaker machine in the y dimension. 
1. Modify "virtual_board = False" to state "virtual_board = True".
1. If you wish to represent a virutal SpiNNaker machine which is wired within a turos shape, please set "requires_wrap_arounds = False" to "requires_wrap_arounds = True"

# Now what?

Run your PyNN scripts as normal, the sPyNNaker front end will generate a SpiNNaker machine with the dimensions you have defined and will execute all of its mapping processes as if it was running on a real machine. 

When your PyNN script has reached the state where, when running on a real SpiNNaker machine, it would be loading data onto the SpiNNaker machine. It will now print out a message saying "XXXXXXXX" 

Good luck. 