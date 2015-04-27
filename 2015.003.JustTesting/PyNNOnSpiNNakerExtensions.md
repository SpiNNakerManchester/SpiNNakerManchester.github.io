---
title: PyNN on SpiNNaker Extension Development Guide
---

This guide is intended to help you set up your development environment so that you can write new extensions to the implementation of SpiNNaker on PyNN.  This might include new neural models, or new connectors.  Note that this guide is not intended to help you make changes to the implementation itself, although it is conceivable that once your extension is stable, it might find its way in to the core code base.

# sPyNNaker C Development Environment
If you are writing new neural models, synapse models or plasticity models, it is likely that you will need to compile C code to run on SpiNNaker.  Firstly, you must [follow the instructions](CDevelopmentForSpiNNaker.html) to install a C development environment.  If your code is then to make use of the sPyNNaker neural modelling code base (which avoids the need to rewrite much of the necessary code):

1. Download the sPyNNaker source code as a [zip](https://github.com/SpiNNakerManchester/sPyNNaker/archive/2015.001.zip) or [tar.gz](https://github.com/SpiNNakerManchester/sPyNNaker/archive/2015.001.tar.gz)
1. Extract the code to the location of your choice.
1. Create a new environment variable ```NEURAL_MODELLING_DIRS``` which is set to the path of the ```neural_modelling``` subfolder of the extracted archive.

# sPyNNaker Python Development Environment
In addition to the C code, you will also likely need to write Python code which enables the use of the new models from within PyNN.  Other extensions to sPyNNaker might also only require python code changes, such as the development of new connector types.  The only requirements for the Python development, is a [working sPyNNaker install](PyNNOnSpiNNakerInstall.html).

If the code that you are writing only extends the Python functionality, this can be written as with any normal Python code, using sPyNNaker as a library as required.  The new code can then be used from PyNN scripts by importing the code separately from sPyNNaker.

# sPyNNaker C and Python Project
When new C code is to be written, new Python code will also be required to interface the C code with PyNN scripts.  We currently recommend keeping these elements in a single project, as this will help to keep them synchronized.

The recommended structure of a new project is as follows (replacing ```<module-name>``` with an appropriate name for your module):  
``` 
sPyNNaker<module-name>Extension/
    neural_modelling/
        <module-name>/
            Makefile
            ...
    <module-name>/
        model_binaries/
            __init__.py
        __init__.py
        ...
    setup.py
```

## Makefile
A basic Makefile template which depends upon various parts of the sPyNNaker C code is shown below.
```
APP = <module_name>$(EXT)
EXTRA_SRC_DIR = $(CURDIR)
MODEL_OBJS = <neural-model-name>.o ...
NEURON_MODEL_H = <neural-model-name>.h
SYNAPSE_SHAPING_H = <synapse-model-name>.h

CFLAGS+= -I$(NEURAL_MODELLING_DIRS)/src

APP_OUTPUT_DIR = $(CURDIR)/../../<module-name>/model_binaries

include $(NEURAL_MODELLING_DIRS)/src/neuron/builds/Makefile.common
```

In more detail:

 - ```APP``` is the name of the binary to be produced; $(EXT) provides the required ".aplx" extension.
 - ```EXTRA_SRC_DIR``` indicates to the sPyNNaker neural_modelling common Makefile that this code is not within the sPyNNaker path.
 - ```MODEL_OBJS``` are the object files to be built to make the final binary, relative to the ```EXTRA_SRC_DIR``` or ```NEURAL_MODELLING_DIRS/src``` directory, depending on where the code lives.
 - ```NEURON_MODEL_H``` is the header file for the neuron model being used.
 - ```SYNAPSE_SHAPING_H``` is the header file for the synapse model being used.
 - ```CFLAGS``` is altered here to allow non-relative references to header files from sPyNNaker.
 - ```APP_OUTPUT_DIR``` is the location where the final aplx file is written.
 - ```include ...``` indicates that the binary is to be built with the common sPyNNaker make process.
