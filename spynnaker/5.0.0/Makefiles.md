The way the C code is built was changed April 2018.

These changes have required major modificattions to the make files and moving many c and make files.

Background
==========

To save ITCM memory the way log messages are handled has been changed.

Instead of using Strings in log messages a Dictionary coder is now used.

However to avoid ever developer having to the dictionary and make sure to use the correct message number this substitution is now done automatically.

This conversion is done by the make files who now call spinn_utilities.make_tools.convertor to convert c files from the src directory into a modified_src directory before building.
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
The convertor expects the first parameter in each log message to be a pure string. 

Changes
=======

Moving of files
---------------
### Sections

The c files have now been split into 4 sections

#### src
All the raw c files have been moved into src directories (unless already in src)
The only files in the src directory and its children should be compilable c files (*.c and *.h).
(ignoring any .gitignore files)

#### makefiles
In the sPynnaker repository makefiles have been moved into a seperate makefiles directory.

#### modified_src
This is where the make files will place the converted c files.
This is done automatically and these directories are deleted by clean so do not edit them.

#### build
This is where temporary files used during make are placed.
In the sPynnaker repository build is no longer a subdirectory of src. 
This includes *.o object files, *.bin, *.elf ect.
These directories are deleted by clean so do not add anything you hope to keep. 

### includes
----------
All .. include paths have been removed!
Instead they have been replaced by full paths back to NEURAL_MODELLING_DIRS/src or the eqivellent.
This allows for the modified files to be easily found using -I NEURAL_MODELLING_DIRS/modified_src

#### Other c changes
The only other c file changes is in neuron/structural_plasticity/synaptogenesis/topographic_map_impl.c
The DMA_WRITEBACK method has been removed. (code hardlined in where needed)
This because of th elimitations of the convertor mentioned above.

### Makefiles

#### Discontinued makefiles
##### FrontEndCommon.mk and Makefile.SpiNNFrontEndCommon
These are no longer in use and if they are included will raise a make error.

The code that previously was here has been transferred to local.mk and neural_build.mk


#### local.mk
For all builds that do not depend on NEURAL_MODELLING_DIRS/src/neuron
Includes the relative stuff previously in FrontEndCommon.mk

This requires 4 variables to be set before being called.
1. APP: name of the application. Used to name the aplx and dict files.
2. BUILD_DIR: see above
3. SOURCES: List of files to build
4. APP_OUTPUT_DIR: Location where to place the aplx and dict files

Optionally extra variables are;
SRC_DIR: defaults to src/ at the same level as the makefile 
MODIFIED_DIR:  defaults to modified_src/ at the same level as the makefile

####  neural_build.mk
For Neuron builds ect that do depend on NEURAL_MODELLING_DIRS/src/neuron
....

#### sPyNNaker8NewModelTemplate/c_models/makefiles/common.mk











Changes to the make files
-------------------------







 