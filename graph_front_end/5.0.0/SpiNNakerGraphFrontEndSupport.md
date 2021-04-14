---
title: What the SpiNNakerGraphFrontEnd Supports
---
This page describes an older version. 
Please see [the latest version](latest/SpiNNakerGraphFrontEndSupport.html) or [home page](/) 

The SpiNNakerGraphFrontEnd is a interface to the SpiNNaker software stack that is designed with the intention of allowing developers / users to 
build applications that run on SpiNNaker machines without having to worry about the low level support of:

1. Booting/powering on the SpiNNaker machine.
1. Mapping the application onto the SpiNNaker machine.
1. Loading the application onto the SpiNNaker machine.
1. Buffering data in/out from/to to the SpiNNaker machine during an application run.
1. Verifying that the application is running on the SpiNNaker machine.
1. Implementing a interface for interacting with the SpiNNaker machine.
1. Acquiring Provenance data from the SpiNNaker machine after an application run.
1. Acquiring debug data from the SpiNNaker machine after / during an application run.
1. Shutting down the SpiNNaker machine correctly after an application run.

# How the SpiNNakerGraphFrontEnd supports the developer/user

The SpiNNakerGraphFrontEnd allows a developer / user to write applications by representing the problem as a graph, where the
nodes in the graph represent a collection of computation and edges represent communication between these computations. 

The developer should read the following presentations to learn how to 
exploit the software stack to it's most potential:

* [Presentation: Introduction to the Graph Front End](GFEIntro.pdf)
* [Presentation: Advanced Graph Front End Usage](GFEAdvanced.pdf) 

A summary is that a developer needs to develop both a Python and c representation of any computation nodes (vertices) and often just a Python version for any unique communication requirements. 

# SpiNNakerGraphFrontEnd interface

The SpiNNakerGraphFrontEnd supports the following interface for developers to use.

|Name|Definition|
|:----------|:----------------------------|
|`setup()`|This is the first call that needs to be executed at all times. It sets up all the basic data structures the software stack requires|
|`add_application_vertex()`|This adds a vertex that can be split over multiple computational nodes|
|`add_machine_vertex()`|This adds a vertex that can only reside on one computational node|
|`add_application_edge()`|This adds a edge between vertices that can be split over multiple computational nodes|
|`add_machine_edge()`|This adds a edge between vertices that can only reside on individual computational nodes|
|`get_machine_dimensions()`|This function supports inquiring the SpiNNaker machine and being given the dimensions of the machine|
|`machine()`|This function returns the Python representation of the SpiNNaker machine|
|`transceiver()`| This function returns the Python communication interface to the SpiNNaker machine| 
|`run()`|This function executes: mapping, loading, running, extraction of provenance and debug data on the SpiNNaker machine|
|`stop()`|This function shuts down the SpiNNaker machine cleanly|

To be extended in the future.
