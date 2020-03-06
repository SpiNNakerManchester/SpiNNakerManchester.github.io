---
title: Using support scripts to install from github on command-line
---

This page details how to use some of the scripts in the [SupportScripts](https://github.com/SpiNNakerManchester/SupportScripts.git) repository to perform a command-line install of the software from GitHub.  This can be useful when e.g. installing the software on a server local to the SpiNNaker machine such as sands or spinn-test in order to test bigger networks than a local machine might be able to deal with sensibly.

# Install

It is recommended that this is done in a [virtual environment](/common_pages/5.0.0/VirtualEnv.html).

First, clone the SupportScripts repository:

    git clone https://github.com/SupportScripts

Next, run the install script:

    bash SupportScripts/install.sh 8 -y

Make sure you have installed the [Python requirements](devenv.html#PythonRequirements), then run the setup script:

    bash SupportScripts/setup.sh

Now you can build the C code

    bash SupportScripts/automatic_make.sh

To test this has worked, run e.g. va_benchmark.py in PyNN8Examples/examples.
