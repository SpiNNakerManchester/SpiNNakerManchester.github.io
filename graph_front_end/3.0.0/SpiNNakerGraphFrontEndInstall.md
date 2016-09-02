---
title: SpiNNakerGraphFrontEnd Installation Guide
layout: default
published: true
---

This guide will detail how to install the 2015.006 "Another Fine Product From The Nonsense Factory" release version of the tools required to run simulations on SpiNNaker using the SpiNNakerGraphFrontEnd interface.

This has been tested using Fedora Linux 20 64-bit, Ubuntu Linux 14.04 LTS 64-bit, Windows 8.1 64-bit, and Mac OS X Mavericks, but it should in principle work on 32-bit and 64-bit versions of Fedora and Ubuntu Linux, Windows 7 and 8, and Mac OS X.

# Contents
* [Ubuntu Linux Requirements](#Ubuntu)
* [Fedora Linux Requirements](#Fedora)
* [Mac OS X Requirements](#MacOSX)
* [32-bit Windows Requirements](#Windows32)
* [64-bit Windows Requirements](#Windows64)
* [Windows PATH settings](#WindowsPath)
* [Standard Central Installation](#Central)
* [User-Only Installation](#User)
* [Virtualenv Installation](#Virtualenv)
* [Configuration](#Configuration)
* [Running some examples](#Examples)
* [Troubleshooting](#Trouble)

# <a name="Ubuntu"></a> Ubuntu Linux Requirements
1. Install Python  
```sudo apt-get install python2.7```
1. Install numpy  
```sudo apt-get install python-numpy```
1. Install scipy  
```sudo apt-get install python-scipy```
1. Install lxml  
```sudo apt-get install python-lxml```
1. Install pip  
```sudo apt-get install python-pip```

Continue to the [Standard Central Installation](#Central), [User-only Installation](#User) or [Virtualenv Installation](#Virtualenv) to install the remaining requirements.

# <a name="Fedora"></a> Fedora Linux Requirements
1. Install Python  
```sudo dnf install python```
1. Install numpy  
```sudo dnf install numpy```
1. Install scipy  
```sudo dnf install scipy```
1. Install lxml  
```sudo dnf install python-lxml```
1. Install pip  
```sudo dnf install python-pip```

Continue to the [Standard Central Installation](#Central), [User-only Installation](#User) or [Virtualenv Installation](#Virtualenv) to install the remaining requirements.

# <a name="MacOSX"></a> Mac OS X Requirements
1. Download and install <a href="https://www.macports.org/install.php" target="_blank">MacPorts</a>
1. Install python  
```sudo port install python27```  
```sudo port select --set python python27```
1. Install numpy  
```sudo port install py27-numpy```
1. Install scipy  
```sudo port install py27-scipy```
1. Install lxml  
```sudo port install py27-lxml```
1. Install pip  
```sudo port install py27-pip```  
```sudo port select --set pip pip27```

Continue to the [Standard Central Installation](#Central), [User-only Installation](#User) or [Virtualenv Installation](#Virtualenv) to install the remaining requirements.

# <a name="Windows32"></a> 32-bit Windows Requirements
1. Download and install [Python](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/python-2.7.6.msi)
1. Download and install [numpy](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/numpy-MKL-1.9.1.win32-py2.7.exe)
1. Download and install [scipy](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/scipy-0.14.1rc1.win32-py2.7.exe)
1. Download and install [lxml](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/lxml-3.4.1.win32-py2.7.exe)
1. Download and install [setuptools](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/setuptools-5.8.win32-py2.7.exe) and [pip] (https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/pip-1.5.6.win32-py2.7.exe)
1. *Optional:* Download and install matplotlib (often used in PyNN scripts for plotting graphs)
    1. Download and install 
[dateutil](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/python-dateutil-2.2.win32-py2.7.exe), 
[pyparsing](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/pyparsing-2.0.2.win32-py2.7.exe), 
[six](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/six-1.6.1.win32-py2.7.exe) and 
[matplotlib](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/matplotlib-1.3.1.win32-py2.7.exe)

Continue to [edit your PATH](#WindowsPath), before installing the remaining requirements.

# <a name="Windows64"></a> 64-bit Windows Requirements
1. Download and install [Python](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/python-2.7.6.amd64.msi)
1. Download and install [numpy](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/numpy-MKL-1.9.1.win-amd64-py2.7.exe)
1. Download and install [scipy](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/scipy-0.14.1rc1.win-amd64-py2.7.exe)
1. Download and install [lxml](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/lxml-3.4.1.win-amd64-py2.7.exe)
1. Download and install [setuptools](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/setuptools-5.8.win-amd64-py2.7.exe) and [pip] (https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/pip-1.5.6.win-amd64-py2.7.exe)
1. *Optional:* Download and install matplotlib (often used in PyNN scripts for plotting graphs)
    1. Download and install
[dateutil](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/python-dateutil-2.2.win-amd64-py2.7.exe), 
[pyparsing](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/pyparsing-2.0.2.win-amd64-py2.7.exe), 
[six](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/six-1.6.1.win-amd64-py2.7.exe) and 
[matplotlib](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/matplotlib-1.3.1.win-amd64-py2.7.exe)

Continue to [edit your PATH](#WindowsPath), before installing the remaining requirements.

# <a name="WindowsPath"></a> Windows Path Settings
1. Edit your PATH environment variable to include the Python27, Python27\Scripts and (if installed) gtk\bin directories.
    1. Go to "Control Panel"
    1. Go to "System" (may be under "System and Security")
    1. Select "Advanced System Settings"
    1. Select "Environment Variables"
    1. Select the "Path" in the "System Variables" box at the bottom
    1. Click on "Edit"
    1. Add the new directory by putting it before the existing string, followed by a single semi-colon; if you installed the dependencies to the default/recommended locations, prepend Path with:  
```C:\Python27;C:\Python27\Scripts; ```

Continue to the [Standard Central Installation](#Central), [User-only Installation](#User) or [Virtualenv Installation](#Virtualenv) to install the remaining requirements.

# <a name="Central"></a> Standard Central Installation
These instructions will install the required packages in a central location.  If you are installing on Linux, you must have root access to do this (or prepend each command with ```sudo```), and Windows users should run these commands from a command prompt run as Administrator (right-click the shortcut for the command prompt and select "Run as administrator" - without the ```sudo```).

If you already have installed the SpiNNakerGraphFrontEnd previously, you will need to uninstall it:  
```[sudo] pip uninstall SpiNNakerGraphFrontEnd```  

1. Install SpiNNakerGraphFrontEnd
```[sudo] pip install "SpiNNakerGraphFrontEnd == 3.0.0"```

You can now [configure](#Configuration) your environment.

# <a name="User"></a> User-only Installation
These instructions will install the required packages only for the current user (in your home directory).  This can avoid issues where you don't have root access to the machine you are installing on, or on a shared machine where the dependencies might otherwise conflict with those of other users.

If you already have installed the SpiNNakerGraphFrontEnd previously, you will need to uninstall it:  
```[sudo] pip uninstall SpiNNakerGraphFrontEnd```  

1. Install   SpiNNakerGraphFrontEnd
```pip install "SpiNNakerGraphFrontEnd == 3.0.0" --user```

You can now [configure](#Configuration) your environment.

# <a name="Virtualenv"></a> Virtualenv Installation
These instructions will install the required packages only in a virtualenv.  Like the user-only installation, this can help when you don't have root access or are on a shared machine.  Additionally, it will help when you have several packages with conflicting dependencies, or those that occupy the same namespace (such as multiple versions of the spinnaker software stack).

If you already have installed the SpiNNakerGraphFrontEnd previously, you will need to uninstall it:  
```[sudo] pip uninstall SpiNNakerGraphFrontEnd```  

The installation of virtualenv and the linking to the external libraries is platform dependent.

* [Ubuntu Virtualenv Installation](#UbuntuVirtualenv)
* [32-bit Fedora Virtualenv Installation](#Fedora32Virtualenv)
* [64-bit Fedora Virtualenv Installation](#Fedora64Virtualenv)
* [Mac OS X Virtualenv Installation](#MacOSXVirtualenv)
* [Windows Virtualenv Installation](#WindowsVirtualenv)

## <a name="UbuntuVirtualenv"></a> Ubuntu Virtualenv Installation
1. Install virtualenv  
```sudo pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice  
```virtualenv <name>```
1. Activate the virtualenv  
```source <name>/bin/activate```
1. Link numpy to the virtualenv  
```ln -s /usr/lib/python2.7/dist-packages/numpy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link scipy to the virtualenv  
```ln -s /usr/lib/python2.7/dist-packages/scipy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link lxml to the virtualenv  
```ln -s /usr/lib/python2.7/dist-packages/lxml* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)  
```pip install python-dateutil```  
```pip install pyparsing```  
```pip install six```  
```ln -s /usr/lib/pymodules/python2.7/matplotlib $VIRTUAL_ENV/lib/python2.7/site-packages/```  
```ln -s /usr/lib/pymodules/python2.7/pylab.py $VIRTUAL_ENV/lib/python2.7/site-packages/```

You must now [install the Graph Front End](#VirtualEnvCommon)

## <a name="Fedora32Virtualenv"></a> 32-bit Fedora Virtualenv Installation
1. Install virtualenv  
```sudo pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice  
```virtualenv <name>```
1. Activate the virtualenv  
```source <name>/bin/activate```
1. Link numpy to the virtualenv  
```ln -s /usr/lib/python2.7/site-packages/numpy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link scipy to the virtualenv  
```ln -s /usr/lib/python2.7/site-packages/scipy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link lxml to the virtualenv  
```ln -s /usr/lib/python2.7/site-packages/lxml* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)  
```pip install python-dateutil```  
```pip install pyparsing```  
```pip install six```  
```ln -s /usr/lib/python2.7/site-packages/matplotlib $VIRTUAL_ENV/lib/python2.7/site-packages/```  
```ln -s /usr/lib/python2.7/site-packages/pylab.py $VIRTUAL_ENV/lib/python2.7/site-packages/```

You must now [install the Graph Front End](#VirtualEnvCommon)

## <a name="Fedora64Virtualenv"></a> 64-bit Fedora Virtualenv Installation
1. Install virtualenv  
```sudo pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice  
```virtualenv <name>```
1. Activate the virtualenv  
```source <name>/bin/activate```
1. Link numpy to the virtualenv  
```ln -s /usr/lib64/python2.7/site-packages/numpy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link scipy to the virtualenv  
```ln -s /usr/lib64/python2.7/site-packages/scipy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link lxml to the virtualenv  
```ln -s /usr/lib64/python2.7/site-packages/lxml* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)  
```pip install python-dateutil```  
```pip install pyparsing```  
```pip install six```  
```ln -s /usr/lib64/python2.7/site-packages/matplotlib $VIRTUAL_ENV/lib/python2.7/site-packages/```  
```ln -s /usr/lib64/python2.7/site-packages/pylab.py $VIRTUAL_ENV/lib/python2.7/site-packages/```

You must now [install the Graph Front End](#VirtualEnvCommon)

## <a name="MacOSXVirtualenv"></a> Mac OS X Virtualenv Installation
1. Install virtualenv  
```sudo pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice  
```virtualenv <name>```
1. Activate the virtualenv  
```source <name>/bin/activate```
1. Link numpy to the virtualenv  
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/numpy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link scipy to the virtualenv  
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/scipy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link lxml to the virtualenv  
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/lxml* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)  
```pip install python-dateutil```  
```pip install pyparsing```  
```pip install six```  
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/matplotlib $VIRTUAL_ENV/lib/python2.7/site-packages/```  
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pylab.py $VIRTUAL_ENV/lib/python2.7/site-packages/```

You must now [install the Graph Front End](#VirtualEnvCommon)

## <a name="WindowsVirtualenv"></a> Windows Virtualenv Installation
1. Open a console as administrator and cd to your home directory  
```cd %HOMEPATH%```
1. Install virtualenv  
```pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice  
```virtualenv <name>```
1. Activate the virtualenv  
```<name>\Scripts\activate.bat ```
1. Link numpy to the virtualenv  
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\numpy C:\Python27\Lib\site-packages\numpy```  
```mklink %VIRTUAL_ENV%\Lib\site-packages\numpy-1.9.1-py2.7.egg-info C:\Python27\site-packages\numpy-1.9.1-py2.7.egg-info```
1. Link scipy to the virtualenv  
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\scipy C:\Python27\Lib\site-packages\scipy```  
```mklink %VIRTUAL_ENV%\Lib\site-packages\scipy-0.14.1rc1-py2.7.egg-info C:\Python27\site-packages\scipy-0.14.1rc1-py2.7.egg-info```
1. Link lxml to the virtualenv  
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\lxml C:\Python27\Lib\site-packages\lxml```  
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\lxml-3.4.1-py2.7.egg-info C:\Python27\site-packages\lxml-3.4.1-py2.7.egg-info```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)  
```pip install python-dateutil```  
```pip install pyparsing```  
```pip install six```  
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\matplotlib C:\Python27\Lib\site-packages\matplotlib```  
```mklink %VIRTUAL_ENV%\Lib\site-packages\pylab.py C:\Python27\Lib\site-packages\pylab.py```
1. *Optional:* To make matplotlib work within a virtualenv, create the following environment variables:  
```TCL_LIBRARY: C:\Python27\tcl\tcl8.5```  
```TK_LIBRARY: C:\Python27\tcl\tk8.5```

You must now [install the Graph Front End](#VirtualEnvCommon)

# <a name="VirtualEnvCommon"></a> Virtual Env Common Install
1. Install SpiNNakerGraphFrontEnd  
```pip install "SpiNNakerGraphFrontEnd == 3.0.0"```
 
You can now [configure](#Configuration) your environment.

# <a name="Configuration"></a> Configuration
When the SpiNNakerGraphFrontEnd is first called, if a configuration file is not found, it will create one in your home directory and exit.  It is possible to ask SpiNNakerGraphFrontEnd to do this before you run your first simulation as follows:  
```python -c "import spinnaker_graph_front_end"```

Note that if you have previously installed a version of the spiNNaker software, you may already have a file called ".spiNNakerGraphFrontEnd.cfg" in your home directory.  In this case, SpyNNaker will attempt to use this file for its parameters.  If you don't have this file, a new file called ".spyNNakerGraphFrontEnd.cfg" will be created in your home directory.  You must edit this file to ensure that SpyNNaker can access your SpiNNaker machine.  Upon opening this file, the part to alter will look like the following:  
```[Machine] ```  
```machineName = None ```  
```version = None ```

If you have a SpiNNaker board, then go to [Local Board](#LocalBoard) if you do not have a SpiNNaker board, please follow the instructions in [Instructions on how to use the different front ends in virtual mode](/common_pages/3.0.0/VirtualMode.html) and then go to [Running some examples](#Examples).

# <a name="LocalBoard"></a> Local Board

Within the file, you should set ```machineName``` to the IP address or hostname of your SpiNNaker machine, and ```version``` to the version of your SpiNNaker board; this will almost certainly be "3" for a 4-chip board or "5" on a 48-chip board.

The default ip address for a spinn-3 board is 192.168.240.253 and the default ip address for a spinn-5 board is 192.168.240.1

## <a name="Network Configuration"></a> Network Configuration

1. Go to the network settings for your computer and add or set an IPv4 entry with the following address for the adapter connected to the SpiNNaker board:  
    1. ip address = 192.168.240.254
    2. sub-mask = 255.255.255.0
    3. default gateway = 0.0.0.0

# <a name="Examples"></a> Running some examples
1. Run:  
```python -m spinnaker_graph_front_end.examples.hello_world.hello_world```
1. You will see the system go through a series of processes from partitioning, to placement, to routing and finally to loading and running, followed by a list of outputs of "Hello World" (one for each core on your board).
If you get this output, you have successfully installed your system.

# <a name="Trouble"></a> Troubleshooting

1. If you experience the error:

```**UnicodeDecodeError: 'ascii' codec can't decode byte 0xb0 in position 1: ordinal not in range(128)**``` 

Then to solve it, edit C:\Python27\Lib\mimetypes.py and add these codes:

    if sys.getdefaultencoding() != 'gbk':  
        reload(sys)
        sys.setdefaultencoding('gbk')
 
before the following line:

    default_encoding = sys.getdefaultencoding()
