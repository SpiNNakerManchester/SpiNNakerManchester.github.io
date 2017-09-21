---
title: Python Dependencies for SpiNNaker
---

This guide will detail how to install the Python dependencies for SpiNNaker.

This has been tested using Fedora Linux 20 64-bit, Ubuntu Linux 14.04 LTS 64-bit, Ubuntu Linux 16.04 LTS 64-bit, Windows 8.1 64-bit, Mac OS X Mavericks and Mac OS X Yosemite, but it should in principle work on 32-bit and 64-bit versions of Fedora and Ubuntu Linux, Windows 7, 8 and 10, and Mac OS X.

* [Ubuntu Linux Requirements](#UbuntuPython)
* [Fedora Linux Requirements](#FedoraPython)
* [Mac OS X Requirements](#MacOSXPython)
* [32-bit Windows Requirements](#Windows32Python)
* [64-bit Windows Requirements](#Windows64Python)
* [Windows PATH settings](#WindowsPath)

## <a name="UbuntuPython"></a> Ubuntu Linux Requirements
1. Install Python
```sudo apt-get install python2.7```
1. Install pip  
```sudo apt-get install python-pip```  
```sudo pip install --upgrade pip setuptools wheel```


## <a name="FedoraPython"></a> Fedora Linux Requirements
1. Install Python
```sudo dnf install python```
1. Install pip  
```sudo dnf install python-pip```  
```sudo pip install --upgrade pip setuptools wheel```

## <a name="MacOSXPython"></a> Mac OS X Requirements
1. Download and install <a href="https://www.macports.org/install.php" target="_blank">MacPorts</a> (Requires [XCode](https://developer.apple.com/technologies/tools/) Developer Tools and an X11 windowing environment such as [XQuartz](https://www.xquartz.org/)).
1. Install python
```sudo port install python27```
```sudo port select --set python python27```
1. Install pip  
```sudo port install py27-pip```  
```sudo port select --set pip pip27```  
```sudo pip install --upgrade pip setuptools wheel```

## <a name="Windows32Python"></a> 32-bit Windows Requirements
1. Download and install [Python](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/python-2.7.6.msi)
1. Download and install [setuptools](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/setuptools-5.8.win32-py2.7.exe) and [pip] (https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win32/pip-1.5.6.win32-py2.7.exe)
1. Update pip - from an administrative console, run:  
```pip install --upgrade pip```
1. Install numpy (optional if you are going to use a Virtual Env):  
```pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win32/numpy-1.13.1.mkl-cp27-cp27m-win32.whl```
1. Install scipy (optional if you are going to use a Virtual Env):  
``` pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win32/scipy-0.19.1-cp27-cp27m-win32.whl```

Continue to [edit your PATH](#WindowsPath).

## <a name="Windows64Python"></a> 64-bit Windows Requirements
Users with an up-to-date version of Windows 10 64-bit may want to use the [Linux Subsystem for Windows 10](https://msdn.microsoft.com/en-gb/commandline/wsl/install_guide?f=255&MSPPError=-2147217396).  This has been tested with an Ubuntu 14.04 install and seems to work well.
For graphics content, you will also need to install and run [an X-Windows Server](https://sourceforge.net/projects/xming/).
After installing, you should follow the [Ubuntu installation instructions](#UbuntuPython).

1. Download and install [Python](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/python-2.7.6.amd64.msi)
1. Download and install [setuptools](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/setuptools-5.8.win-amd64-py2.7.exe) and [pip] (https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/pip-1.5.6.win-amd64-py2.7.exe)
1. Update pip - from an administrative console, run:  
```sudo pip install --upgrade pip```
1. Install numpy (optional if you are going to use a Virtual Env):
```pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win64/numpy-1.13.1.mkl-cp27-cp27m-win_amd64.whl```
1. Install scipy (optional if you are going to use a Virtual Env):
``` pip install https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win64/scipy-0.19.1-cp27-cp27m-win_amd64.whl```

Continue to [edit your PATH](#WindowsPath).

## <a name="WindowsPath"></a> Windows Path Settings
1. Edit your PATH environment variable to include the Python27, Python27\Scripts and (if installed) gtk\bin directories.
    1. Go to "Control Panel"
    1. Go to "System" (may be under "System and Security")
    1. Select "Advanced System Settings"
    1. Select "Environment Variables"
    1. Select the "Path" in the "System Variables" box at the bottom
    1. Click on "Edit"
    1. Add the new directory by putting it before the existing string, followed by a single semi-colon; if you installed the dependencies to the default/recommended locations, prepend Path with:
```C:\Python27;C:\Python27\Scripts; ```
