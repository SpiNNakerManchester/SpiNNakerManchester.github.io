---
title: PyNN on SpiNNaker Extension Development Guide
---

This guide is intended to help you set up your development environment so that you can write new extensions to the implementation of SpiNNaker on PyNN.  This might include new neural models, or new connectors.  Note that this guide is not intended to help you make changes to the implementation itself, although it is conceivable that once your extension is stable, it might find its way in to the core code base.

# sPyNNaker C Development Environment
If you are writing new neural models, synapse models or plasticity models, it is likely that you will need to compile C code to run on SpiNNaker.

You have two choices at this stage:

1. If you want to use the most up-to-date master version of the code, follow the [development environment instructions](../../development/devenv.html).
1. If you are using version 4.0.0, follow [these instructions](/common_pages/4.0.0/CDevelopmentForSpinnaker.html)

# sPyNNaker Python Development Environment
In addition to the C code, you will also likely need to write Python code which enables the use of the new models from within PyNN.  Other extensions to sPyNNaker might also only require python code changes, such as the development of new connector types.  The only requirements for the Python development is a working sPyNNaker install.

If the code that you are writing only extends the Python functionality, this can be written as with any normal Python code, using sPyNNaker as a library as required.  The new code can then be used from PyNN scripts by importing the code separately from sPyNNaker.

# Writing New Neuron Models and Plasticity Rules
* [Tutorial: Adding new Neural Models](NewNeuronModels-LabManual.pdf)
* [Tutorial: Adding new Plasticity Models](NewPlasticityRules-LabManual.pdf)
