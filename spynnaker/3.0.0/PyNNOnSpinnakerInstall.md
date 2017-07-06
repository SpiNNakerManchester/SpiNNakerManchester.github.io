---
title: PyNN on SpiNNaker Installation Guide
layout: default
published: true
---

This guide will detail how to install the release version of the tools required to run simulations on SpiNNaker using the PyNN scripting language.

# Installation

You must first install the [Python Dependencies](/common_pages/3.0.0/PythonInstall.html).  Continue to the [Standard Central Installation](#Central), [User-only Installation](#User) or [Virtualenv Installation](#Virtualenv) to install the remaining requirements, depending on the needs of your working environment.

* [Python Dependencies](/common_pages/3.0.0/PythonInstall.html)
* [Standard Central Installation](#Central)
* [User-Only Installation](#User)
* [Virtualenv Installation](#Virtualenv)
* [Configuration](#Configuration)
* [Running some examples](#Examples)
* [Troubleshooting](#Trouble)


# <a name="Central"></a> Standard Central Installation
These instructions will install the required packages in a central location.  If you are installing on Linux, you must have root access to do this (or prepend each command with ```sudo```), and Windows users should run these commands from a command prompt run as Administrator (right-click the shortcut for the command prompt and select "Run as administrator" - without the ```sudo```).

If you already have installed sPyNNaker previously (and the optional sPyNNakerExtraDevicesPlugin and/or sPyNNakerExtraModelsPlugin), you will need to uninstall it:  
```[sudo] pip uninstall pyNN-SpiNNaker```  
```[sudo] pip uninstall sPyNNaker```  
```[sudo] pip uninstall sPyNNakerExternalDevicesPlugin```  
```[sudo] pip uninstall sPyNNakerExtraModelsPlugin```

1. Install sPyNNaker  
```[sudo] pip install "sPyNNaker == 3.0.0"```
1. Install pyNN-SpiNNaker  
```[sudo] pip install "pyNN-SpiNNaker == 3.0.0"```
1. *Optional* Install sPyNNakerExternalDevicesPlugin (used for live input and output)  
```[sudo] pip install "sPyNNakerExternalDevicesPlugin == 3.0.0"```
1. *Optional* Install sPyNNakerExtraModelsPlugin (provides some non-standard PyNN models)  
```[sudo] pip install "sPyNNakerExtraModelsPlugin == 3.0.0"```

You can now [configure](#Configuration) your environment.

# <a name="User"></a> User-only Installation
These instructions will install the required packages only for the current user (in your home directory).  This can avoid issues where you don't have root access to the machine you are installing on, or on a shared machine where the dependencies might otherwise conflict with those of other users.

If you already have installed sPyNNaker previously (and the optional sPyNNakerExtraDevicesPlugin and/or sPyNNakerExtraModelsPlugin), you will need to uninstall it:  
```pip uninstall pyNN-SpiNNaker```  
```pip uninstall sPyNNaker```  
```pip uninstall sPyNNakerExternalDevicesPlugin```  
```pip uninstall sPyNNakerExtraModelsPlugin```

1. Install sPyNNaker  
```pip install "sPyNNaker == 3.0.0" --user```
1. Install pyNN-SpiNNaker  
```pip install "pyNN-SpiNNaker == 3.0.0" --user```
1. *Optional* Install sPyNNakerExternalDevicesPlugin (used for live input and output)  
```pip install "sPyNNakerExternalDevicesPlugin == 3.0.0" --user```
1. *Optional* Install sPyNNakerExtraModelsPlugin (provides some non-standard PyNN models)  
```pip install "sPyNNakerExtraModelsPlugin == 3.0.0" --user```

You can now [configure](#Configuration) your environment.

# <a name="Virtualenv"></a> Virtualenv Installation
Follow [these instructions](/common_pages/3.0.0/VirtualEnv.html) to install the dependencies in a virtual environment.

If you already have installed sPyNNaker previously (and the optional sPyNNakerExtraDevicesPlugin and/or sPyNNakerExtraModelsPlugin), you will need to uninstall it:

1. Activate your virtualenv, ```<name>```  
```source <name>/bin/activate```
1. Uninstall the existing tools  
```pip uninstall pyNN-SpiNNaker```  
```pip uninstall sPyNNaker```  
```pip uninstall sPyNNakerExternalDevicesPlugin```  
```pip uninstall sPyNNakerExtraModelsPlugin```

To install the tools:

1. Activate your virtualenv, ```<name>```  
```source <name>/bin/activate```
1. Install sPyNNaker  
```pip install "sPyNNaker == 3.0.0"```
1. Install pyNN-SpiNNaker  
```pip install "pyNN-SpiNNaker == 3.0.0"```
1. *Optional* Install sPyNNakerExternalDevicesPlugin (used for live input and output)  
```pip install "sPyNNakerExternalDevicesPlugin == 3.0.0"```
1. *Optional* Install sPyNNakerExtraModelsPlugin (provides some non-standard PyNN models)  
```pip install "sPyNNakerExtraModelsPlugin == 3.0.0"```
 
You can now [configure](#Configuration) your environment.

# <a name="Configuration"></a> Configuration
When SpyNNaker is first called, if a configuration file is not found, it will create one in your home directory and exit.  It is possible to ask SpyNNaker to do this before you run your first simulation as follows:  
```python -c "import pyNN.spiNNaker"```

Note that if you have previously installed a version of the spiNNaker software, you may already have a file called ".pacman.cfg" in your home directory.  In this case, SpyNNaker will attempt to use this file for its paramters.  If you don't have this file, a new file called ".spynnaker.cfg" will be created in your home directory.  You must edit this file to ensure that SpyNNaker can access your SpiNNaker machine.  Upon opening this file, the part to alter will look like the following:  
```[Machine] ```  
```machineName = None ```  
```version = None ```

If you have a SpiNNaker board, then go to [Local Board](#LocalBoard) if you do not have a SpiNNaker board, please follow the instructions in [Instructions on how to use the different front ends in virtual mode](/common_pages/3.0.0/VirtualMode.html) and then go to [Running some examples](#Examples).

# <a name="LocalBoard"></a> Local Board

Within the file, you should set ```machineName``` to the IP address or hostname of your SpiNNaker machine, and ```version``` to the version of your SpiNNaker board; this will almost certainly be "3" for a 4-chip board or "5" on a 48-chip board. 

The default ip address for a spinn-3 board is 192.168.240.253 and the default ip address for a spinn-5 board is 192.168.240.1

now go to [Network Configuration](#Network Configuration).

## <a name="Network Configuration"></a> Network Configuration

1. Go to the network settings for your computer and add or set an IPv4 entry with the following address for the adapter connected to the SpiNNaker board:  
    1. ip address = 192.168.240.254
    2. sub-mask = 255.255.255.0
    3. default gateway = 0.0.0.0

# <a name="Examples"></a> Running some examples
1. Download the examples from [here](https://github.com/SpiNNakerManchester/PyNNExamples/archive/3.0.0.zip) (zip) or [here](https://github.com/SpiNNakerManchester/PyNNExamples/archive/3.0.0.tar.gz) (tar.gz)
1. Extract the archive
1. Go to the "examples" folder
1. Run:  
```python va_benchmark.py```
1. You will see the system go through a series of processes from partitioning, to placement, to routing and finally to loading and running.
1. Once the example has finished, you should see a graph, that will look something like this:  
![VABenchmarkSpikes](va_benchmark.png)
If you get the output above, you have successfully installed your system.

# <a name="Trouble"></a> Troubleshooting

1. If you experience the error:

```**UnicodeDecodeError: 'ascii' codec can't decode byte 0xb0 in position 1: ordinal not in range(128)**``` 

Then to solve it, edit C:\Python27\Lib\mimetypes.py and add these codes:

    if sys.getdefaultencoding() != 'gbk':  
        reload(sys)
        sys.setdefaultencoding('gbk')
 
before the following line:

    default_encoding = sys.getdefaultencoding()
    
2. OSX: if experiencing the following tkinter error:

```_tkinter.TclError: no display name and no $DISPLAY environment variable```

 it may be solved by setting the backend for matplotlib. This can be done by editing the matplotlibrc file in the current working directory to read to ```backend: TkAgg```. This is usually found in $DEV/lib/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc
 
 In a virtualenv, create a new file in the root directory ```.matplotlib/matplotlibrc``` that reads ```backend: TkAgg```. ([Sample matplotlibrc file](https://matplotlib.org/_static/matplotlibrc))

