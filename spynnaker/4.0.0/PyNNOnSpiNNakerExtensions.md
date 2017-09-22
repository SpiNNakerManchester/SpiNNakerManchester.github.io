---
title: PyNN on SpiNNaker Extension Development Guide
---

This guide is intended to help you set up your development environment so that you can write new extensions to the implementation of SpiNNaker on PyNN.  This might include new neural models, or new connectors.  Note that this guide is not intended to help you make changes to the implementation itself, although it is conceivable that once your extension is stable, it might find its way in to the core code base.

# sPyNNaker C Development Environment
If you are writing new neural models, synapse models or plasticity models, it is likely that you will need to compile C code to run on SpiNNaker.  Firstly, you must [follow the instructions](/common_pages/4.0.0/CDevelopmentForSpiNNaker.html) to install a C development environment.  If your code is then to make use of the sPyNNaker neural modelling code base (which avoids the need to rewrite much of the necessary code):

1. Download the sPyNNaker source code as a [zip](https://github.com/SpiNNakerManchester/sPyNNaker/archive/4.0.0.zip) or [tar.gz](https://github.com/SpiNNakerManchester/sPyNNaker/archive/4.0.0.tar.gz)
1. Extract the code to the location of your choice.
1. Create a new environment variable `NEURAL_MODELLING_DIRS` which is set to the path of the `neural_modelling` subfolder of the extracted archive (note that in Windows, this should be the MinGW Posix path e.g. if you have extracted the archive to `C:\sPyNNaker\`, you should set the environment variable to `/c/sPyNNaker/neural_modelling`).

# sPyNNaker Python Development Environment
In addition to the C code, you will also likely need to write Python code which enables the use of the new models from within PyNN.  Other extensions to sPyNNaker might also only require Python code changes, such as the development of new connector types.  The only requirements for the Python development, is a [working sPyNNaker install](PyNNOnSpinnakerInstall.html).

If the code that you are writing only extends the Python functionality, this can be written as with any normal Python code, using sPyNNaker as a library as required.  The new code can then be used from PyNN scripts by importing the code separately from sPyNNaker.

# Writing New Neuron Models and Plasticity Rules
* [Tutorial: Adding new Neural Models](NewNeuronModels-LabManual.pdf)
* [Tutorial: Adding new Plasticity Models](NewPlasticityRules-LabManual.pdf)
