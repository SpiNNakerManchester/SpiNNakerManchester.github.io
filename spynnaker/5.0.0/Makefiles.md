---
title: Makefiles in sPyNNaker version 5.0.0
layout: default
---

The way the C code is built was changed April 2018.

These changes have required major modificattions to the make files and moving many c and make files.

Background
==========

To save ITCM memory the way log messages are handled has been changed.

Instead of using Strings in log messages a Dictionary coder is now used.

However to avoid ever developer having to the dictionary and make sure to use the correct message number this substitution is now done automatically.

This conversion is done by the make files who now call spinn_utilities.make_tools.converter to convert c files from the src directory into a modified_src directory before building.
The tool also creates *.dict files to record the mappings as well as *.range files to keep the number unique in each parts of the code.

Each log messages is changed to a log_mini method where the message string is replaced by a number.
For example:
    log_info("Reading parameters from 0x%.8x", region_address);
becomes
    log_mini_info(12345, region_address);

The conversion from message ids back to the full string is done automatically by spinn_utilities.make_tools.replacer called from spinn_front_end_common/interface/interface_functions/chip_iobuf_extractor.py

Future_work
-----------
The log_mini_ methods currently still use fprintf and record each number ids and values in String format. This may be replaced with saving in numerical format instead to save even more iobuff space, and possibly allow more data types to be logged.

Limitations
-----------
The converter expects the first parameter in each log message to be a pure string.

As String parameter can be passed in using as a variable using %s for example:
Instead of:
log_info(msg);
do:
log_info("%s", msg);

Location of files
=================
The c files have now been split into 4 sections

## src
All the raw c files have been moved into src directories (unless already in src)
The only files in the src directory and its children should be compilable c files (*.c and *.h).
(ignoring any .gitignore files)

## makefiles
Each root makefile is now at the same level as their src directory
or in a makefile directoy parallel to their src directory.

## modified_src
This is where the make files will place the converted c files.
This is done automatically and these directories are deleted by clean so do not edit them.

## build
This is where temporary files used during make are placed.
In the sPynnaker repository build is no longer a subdirectory of src.
This includes *.o object files, *.bin, *.elf ect.
These directories are deleted by clean so do not add anything you hope to keep.

Changes to the C files
----------------------

## includes
All .. include paths have been removed!
Instead they have been replaced by full paths back to NEURAL_MODELLING_DIRS/src or the eqivellent.
This allows for the modified files to be easily found using -I NEURAL_MODELLING_DIRS/modified_src

## Other c changes
The only other c file changes is in neuron/structural_plasticity/synaptogenesis/topographic_map_impl.c
The DMA_WRITEBACK method has been changed. (See limitations)

Makefiles
=========

## spinnaker_tools.mk
This is the root make file for nearly all the make files.

Contains the main instuctions for building spinnaker c files into o files,
then elf files, then bin and md files and filay aplx files

This is a nearly like for like replacement of spinnaker_tools/make/Makefile.common

## local.mk
For all builds where the c files are local to the make file.
This covers most cases that do NOT depend on NEURAL_MODELLING_DIRS/src/neuron
Includes the relative stuff previously in Makefile.FrontEndCommon or FrontEndCommon.mk

This requires 4 variables to be set before being called.
1. APP: name of the application. Used to name the aplx and dict files.
2. SOURCES: List of files to build
3. APP_OUTPUT_DIR: Location where to place the aplx and dict files

Optionally extra variables are;
SRC_DIR: defaults to src/ at the same level as the makefile
MODIFIED_DIR:  defaults to modified_src/ at the same level as the makefile
BUILD_DIR: defaults to build/ at the same level as the makefile

Muiltple make files can be in the same directory,
sharing the same src and build dirs as long as the define a different APP.
The code will be modifed once unless it is changed between builds.

## neural_build.mk
For Neuron builds ect that do depend on NEURAL_MODELLING_DIRS/src/neuron

Includes the relative stuff previously in FrontEndCommon.mk, paths.mk
and sPyNNaker/neural_modelling/src/neuron/builds/common.mk

Neurons are built by linking together various bits of c code defined in the variables
* NEURON_MODEL
* NEURON_MODEL_H
* INPUT_TYPE_H
* THRESHOLD_TYPE_H
* SYNAPSE_TYPE_H
* SYNAPSE_DYNAMICS

Plus the following optional variables:
* ADDITIONAL_INPUT_H
* WEIGHT_DEPENDENCE
* TIMING_DEPENDENCE
* SYNAPTOGENESIS_DYNAMICS

These should all be defined based on the variable
* NEURON_DIR  (Which points to $(NEURAL_MODELLING_DIRS)/src/)
  * For historical SOURCE_DIR is also set but its use is not encouraged

If the c sources are not all in NEURAL_MODELLING_DIRS/src see [sPyNNaker8NewModelTemplate](https://github.com/SpiNNakerManchester/sPyNNaker8NewModelTemplate)
and in particular sPyNNaker8NewModelTemplate/c_models/makefiles/my_neuron_modelling_build.mk for an example.

The following variables are also needed but have default values
* BUILD_DIR defaults to $(NEURAL_MODELLING_DIRS)/builds/$(APP)/
   * Each individual build MUST have a unique build directory due to the complex linking.
* APP_OUTPUT_DIR defaults to:=  $(abspath $(NEURAL_MODELLING_DIRS)/../spynnaker/pyNN/model_binaries)/

Internally the paths are changed to ones based on:
* MODIFIED_DIR := $(NEURAL_MODELLING_DIRS)/modified_src

All the make rules required to modify the c code and build the dict files are provided.

## sPyNNaker8NewModelTemplate/c_models/makefiles/my_neuron_modelling_build.mk
This is an example file of how to use multiple source directories and still build using neurons.

Documentation has been include in the make file itself.

## Other make files
Many of the previous shared make files are no longer used.

They have been converted to just throwing an error and pointing here.

Please contact the spinnaker team (idealy via the googlegroup) if you need help converting previous make files.

## Dict Files
The make files generate a APP_OUTPUT_DIR/APP.dict file next to each
APP_OUTPUT_DIR/APP.aplx file.

The purpose of these files is to supply the dictionary mapping
for the log messages so that they can be correctly converted back.

These hold the mappings as they where at the time the aplx file was created.
If the sources have changed and partially rebuilt since aplx file was commited they may not match the files in the modified directories.

Whole c code directories are converted in a single call.
This approach was chosen as if avoids having to track exactly which files are included.
It also allows the modified code to be reused for several build.
Log Levels are ignored as they could be different between builds.
Therefor the dict files will include more classes and messages than actualy used in the cod
As they list by log message and not by c file, files with no log statements
will not be included, but will have been converted into the modified directories.
So the dict files can not be considered listing of what c files where used,
or what messages could be logged.

### SPINN_DIRS/lib/log.ranges
This file is automatically generated, used and deleted by clean-install
so you need not worry about it.
What is does do is make sure that each modified directory has a unique range
of numbers to use.
As long as all you directories have a shared root this file will just list based on that shared root


