---
title: Setting up a Python Virtualenv for SpiNNaker
---

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

1. *Optional:* To make matplotlib work within a virtualenv, create the following environment variables:

       TCL_LIBRARY: C:\Python38\tcl\tcl8.6
       TK_LIBRARY: C:\Python38\tcl\tk8.6
