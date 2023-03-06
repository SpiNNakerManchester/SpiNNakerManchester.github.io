---
title: Using support scripts to install from github on command-line
---

This page details how to use some of the scripts in the [SupportScripts](https://github.com/SpiNNakerManchester/SupportScripts.git) repository to perform a command-line install of the software from GitHub.  This can be useful when e.g. installing the software on a server local to the SpiNNaker machine such as sands or spinn-test in order to test bigger networks than a local machine might be able to deal with sensibly.

# Install

Make sure you have installed the [Python requirements](/common_pages/6.0.0/PythonInstall.html),
and the [C requirements](/common_pages/6.0.0/Compiler.html).

It is recommended that the remaining steps are done in a [virtual environment](/common_pages/6.0.0/VirtualEnv.html).

First, clone the SupportScripts repository:

    git clone https://github.com/SpiNNakerManchester/SupportScripts

Next, run the install script:

    bash SupportScripts/install.sh 8 -y

Then run the setup script:

    bash SupportScripts/setup.sh

Then ensure that the PyNN SpiNNaker link is set up:

    python -m spynnaker.pyNN.setup_pynn

Make sure the [C environment variables](devenv6.0.html#cenvironment) are set correctly, particularly if you are in a new virtual environment and you had an older SpiNNaker software install with different values for the environment variables.

Now you can build the C code by running the automatic make script:

    bash SupportScripts/automatic_make.sh

To test this has worked, run e.g. va_benchmark.py in PyNN8Examples/examples.
