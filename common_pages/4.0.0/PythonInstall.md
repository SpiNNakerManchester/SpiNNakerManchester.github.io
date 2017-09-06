---
title: Python Dependencies for SpiNNaker
---

This guide will detail how to install the Python dependencies for SpiNNaker.

This has been tested using Fedora Linux 20 64-bit, Ubuntu Linux 14.04 LTS 64-bit, Windows 8.1 64-bit, and Mac OS X Mavericks, but it should in principle work on 32-bit and 64-bit versions of Fedora and Ubuntu Linux, Windows 7, 8 and 10, and Mac OS X.

* [Ubuntu Linux Requirements](#UbuntuPython)
* [Fedora Linux Requirements](#FedoraPython)
* [Mac OS X Requirements](#MacOSXPython)
* [32-bit Windows Requirements](#Windows32Python)
* [64-bit Windows Requirements](#Windows64Python)
* [Windows PATH settings](#WindowsPath)

## <a name="UbuntuPython"></a> Ubuntu Linux Requirements
1. Install Python  
```sudo apt-get install python2.7```
1. Install numpy 1.12 or lower  
```sudo apt-get install python-numpy```
1. Install scipy  
```sudo apt-get install python-scipy```
1. Install lxml  
```sudo apt-get install python-lxml```
1. Install pip  
```sudo apt-get install python-pip```
1. *Optional:* Install matplotlib (often used in PyNN scripts for plotting graphs)  
```sudo apt-get install python-matplotlib```

## <a name="FedoraPython"></a> Fedora Linux Requirements
1. Install Python  
```sudo dnf install python```
1. Install numpy 1.12 or lower  
```sudo dnf install python-numpy```
1. Install scipy  
```sudo dnf install scipy```
1. Install lxml  
```sudo dnf install python-lxml```
1. Install pip  
```sudo dnf install python-pip```
1. *Optional:* Install matplotlib (often used in PyNN scripts for plotting graphs)  
```sudo dnf install python-matplotlib```

## <a name="MacOSXPython"></a> Mac OS X Requirements
1. Download and install <a href="https://www.macports.org/install.php" target="_blank">MacPorts</a> (Requires [XCode](https://developer.apple.com/technologies/tools/) Developer Tools and an X11 windowing environment such as [XQuartz](https://www.xquartz.org/)).
1. Install python  
```sudo port install python27```  
```sudo port select --set python python27```
1. Install numpy 1.12 or lower  
```sudo port install py27-numpy<=1.12.1```
1. Install scipy  
```sudo port install py27-scipy```
1. Install lxml  
```sudo port install py27-lxml```
1. Install pip  
```sudo port install py27-pip```  
```sudo port select --set pip pip27```
1. *Optional:* Install matplotlib (often used in PyNN scripts for plotting graphs)  
```sudo port install py27-matplotlib```

## <a name="Windows32Python"></a> 32-bit Windows Requirements
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

Continue to [edit your PATH](#WindowsPath).

## <a name="Windows64Python"></a> 64-bit Windows Requirements
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
