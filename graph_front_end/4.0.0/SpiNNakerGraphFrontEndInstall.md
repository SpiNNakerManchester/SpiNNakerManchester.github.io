---
title: SpiNNakerGraphFrontEnd Installation Guide
layout: default
published: true
---

This guide details how to install the release version of the tools required to run simulations on SpiNNaker using the SpiNNakerGraphFrontEnd interface.

# Installation

You must first install the [Python Dependencies](/common_pages/4.0.0/PythonInstall.html).  Continue to the [Standard Central Installation](#Central), [User-only Installation](#User) or [Virtualenv Installation](#Virtualenv) to install the remaining requirements, depending on the needs of your working environment.

* [Python Dependencies](/common_pages/4.0.0/PythonInstall.html)
* [Standard Central Installation](#Central)
* [User-Only Installation](#User)
* [Virtualenv Installation](#Virtualenv)
* [Configuration](#Configuration)
* [Running some examples](#Examples)
* [Troubleshooting](#Trouble)

# <a name="Central"></a> Standard Central Installation
These instructions will install the required packages in a central location.  If you are installing on Linux, you must have root access to do this (or prepend each command with `sudo`), and Windows users should run these commands from a command prompt run as Administrator (right-click the shortcut for the command prompt and select "Run as administrator" — without the `sudo`).

1. If you already have installed the SpiNNakerGraphFrontEnd previously, you will need to uninstall it:

       [sudo] pip uninstall SpiNNakerGraphFrontEnd

1. Install SpiNNakerGraphFrontEnd

       [sudo] pip install SpiNNakerGraphFrontEnd

You can now [configure](#Configuration) your environment.

# <a name="User"></a> User-only Installation
These instructions will install the required packages only for the current user (in your home directory).  This can avoid issues where you don't have root access to the machine you are installing on, or on a shared machine where the dependencies might otherwise conflict with those of other users.

1. If you already have installed the SpiNNakerGraphFrontEnd previously, you will need to uninstall it:

       [sudo] pip uninstall SpiNNakerGraphFrontEnd

1. Install   SpiNNakerGraphFrontEnd

       pip install SpiNNakerGraphFrontEnd --user

You can now [configure](#Configuration) your environment.

# <a name="Virtualenv"></a> Virtualenv Installation
Follow [these instructions](/common_pages/4.0.0/VirtualEnv.html) to install the dependencies in a virtual environment.

If you already have installed the SpiNNakerGraphFrontEnd previously, you will need to uninstall it:

1. Activate your virtualenv, `<name>`

       source <name>/bin/activate

1. Uninstall the existing tools

       [sudo] pip uninstall SpiNNakerGraphFrontEnd

Remember, to install the tools, first activate your virtualenv, `<name>`

    source <name>/bin/activate
        
## Windows 64-bit:

1. Install numpy:

       pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win64/numpy-1.13.1.mkl-cp27-cp27m-win_amd64.whl

1. Install scipy:  

       pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win64/scipy-0.19.1-cp27-cp27m-win_amd64.whl```

## Windows 32-bit:

1. Install numpy (optional if you are going to use a Virtual Env):  

       pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win32/numpy-1.13.1.mkl-cp27-cp27m-win32.whl```

1. Install scipy (optional if you are going to use a Virtual Env):  

       pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win32/scipy-0.19.1-cp27-cp27m-win32.whl```

## All Platforms

1. Install SpiNNakerGraphFrontEnd

       pip install SpiNNakerGraphFrontEnd

You can now [configure](#Configuration) your environment.

# <a name="Configuration"></a> Configuration
When the SpiNNakerGraphFrontEnd is first called, if a configuration file is not found, it will create one in your home directory and exit.  It is possible to ask SpiNNakerGraphFrontEnd to do this before you run your first simulation as follows:

    python -c "import spinnaker_graph_front_end"

Note that if you have previously installed a version of the spiNNaker software, you may already have a file called `.spiNNakerGraphFrontEnd.cfg` in your home directory.  In this case, SpyNNaker will attempt to use this file for its parameters.  If you don't have this file, a new file called `.spyNNakerGraphFrontEnd.cfg` will be created in your home directory.  You must edit this file to ensure that SpyNNaker can access your SpiNNaker machine.  Upon opening this file, the part to alter will look like the following:

```
[Machine]
machineName = None
version = None
```

If you have a SpiNNaker board, then go to [Local Board](#LocalBoard) if you do not have a SpiNNaker board, please follow the instructions in [Instructions on how to use the different front ends in virtual mode](/common_pages/4.0.0/VirtualMode.html) and then go to [Running some examples](#Examples).

# <a name="LocalBoard"></a> Local Board

Within the file, you should set `machineName` to the IP address or hostname of your SpiNNaker machine, and `version` to the version of your SpiNNaker board; this will almost certainly be "3" for a 4-chip board or "5" on a 48-chip board.

The default IP address for a spinn-3 board is `192.168.240.253` and the default IP address for a spinn-5 board is `192.168.240.1`.

## <a name="Network Configuration"></a> Network Configuration

1. Go to the network settings for your computer and add or set an IPv4 entry with the following address for the adapter connected to the SpiNNaker board:

   * IP address = `192.168.240.254`
   * sub-mask = `255.255.255.0`
   * default gateway = `0.0.0.0`

# <a name="Examples"></a> Running some examples
1. Run:

       python -m spinnaker_graph_front_end.examples.hello_world.hello_world

1. You will see the system go through a series of processes from partitioning, to placement, to routing and finally to loading and running, followed by a list of outputs of "Hello World" (one for each core on your board).

If you get this output, you have successfully installed your system.

# <a name="Trouble"></a> Troubleshooting

1. If you experience the error:

       **UnicodeDecodeError: 'ascii' codec can't decode byte 0xb0 in position 1: ordinal not in range(128)**

   Then to solve it, edit `C:\Python27\Lib\mimetypes.py` and add these codes:

   ```python
   if sys.getdefaultencoding() != 'gbk':
       reload(sys)
       sys.setdefaultencoding('gbk')
   ```

   before the following line:

   ```python
   default_encoding = sys.getdefaultencoding()
   ```

