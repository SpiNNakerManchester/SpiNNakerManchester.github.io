---
title: Setting up a Python Virtualenv for SpiNNaker
---
This page describes an older version. 
Please see [the latest version](/latest/VirtualEnv.html) or [home page](/) 

These instructions will install the required packages only in a virtualenv.  This can help when you don't have root access or are on a shared machine.  Additionally, it will help when you have several packages with conflicting dependencies, or those that occupy the same namespace (such as pyNN.spiNNaker if you have an older version of the toolchain).

# Installation on non-Windows

To install and create a virtualenv on any platform other than Windows:

1. Install virtualenv:

       sudo pip install virtualenv

1. Create a virtualenv; `<name>` in the following can be replaced by the name of your choice

       virtualenv <name>

1. Activate the virtualenv:

       source <name>/bin/activate

# Installation on Windows

On Windows, the instructions are similar, but subtly different:

1. Open a console as administrator and cd to your home directory

       cd %HOMEPATH%

1. Install virtualenv

       pip install virtualenv

1. Create a virtualenv; `<name>` in the following can be replaced by the name of your choice

       virtualenv <name>

1. Activate the virtualenv

       <name>\Scripts\activate.bat

1. Install numpy:

   * On 32-bit Windows:

         pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win32/numpy-1.13.1.mkl-cp27-cp27m-win32.whl

   * On 64-bit Windows:

         pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win64/numpy-1.13.1.mkl-cp27-cp27m-win_amd64.whl

1. Install scipy:

   * On 32-bit Windows:

         pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win32/scipy-0.19.1-cp27-cp27m-win32.whl

   * On 64-bit Windows:

         pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win64/scipy-0.19.1-cp27-cp27m-win_amd64.whl

1. *Optional:* To make matplotlib work within a virtualenv, create the following environment variables:

       TCL_LIBRARY: C:\Python27\tcl\tcl8.5
       TK_LIBRARY: C:\Python27\tcl\tk8.5
