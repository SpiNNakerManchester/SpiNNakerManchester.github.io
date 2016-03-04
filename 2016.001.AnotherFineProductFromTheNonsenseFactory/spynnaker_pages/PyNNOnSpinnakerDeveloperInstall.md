---
title: PyNN on SpiNNaker Developer Install Guide
---

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
* [Binary Compilation](#CCOMPILEBINARIES)
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
1. *Optional:* Install matplotlib (often used in PyNN scripts for plotting graphs)  
```sudo apt-get install python-matplotlib```

Continue to the [Git Clone](#GITCLONE) to install the remaining requirements.

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
1. *Optional:* Install matplotlib (often used in PyNN scripts for plotting graphs)  
```sudo dnf install python-matplotlib```

Continue to the [Git Clone](#GITCLONE) to install the remaining requirements.

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
1. *Optional:* Install matplotlib (often used in PyNN scripts for plotting graphs)  
```sudo port install py27-matplotlib```

Continue to the [Git Clone](#GITCLONE) to install the remaining requirements.

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

Continue to the [Git Clone](#GITCLONE) to install the remaining requirements.

# <a name="GITCLONE"></a> Git Cloning Requirements

* [Central gitClone](#centeralGit)
 * [User-Only gitclone](#userGit)
 * [Virtualenv gitclone](#virutalGit)
 

# <a name="centralGit"></a> Central gitClone

1. You now need to clone the github repositories for all the software stack. This requires you to run the following commands in a terminal, in the folder of your choice where the software will be installed.
    1. git clone https://github.com/SpiNNakerManchester/sPyNNaker.git
    1. cd sPyNNaker
    1. sudo python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/sPyNNakerExtraModelsPlugin.git
    1. cd sPyNNakerExtraModelsPlugin
    1. sudo python setup.py develop --no-deps 
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git
    1. cd SpiNNFrontEndCommon
    1. sudo python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/PACMAN.git
    1. cd PACMAN
    1. sudo python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNMan.git
    1. cd SpiNNMan
    1. sudo python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin.git
    1. cd sPyNNakerExternalDevicesPlugin
    1. sudo python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/DataSpecification.git
    1. cd DataSpecification
    1. sudo python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNMachine.git
    1. cd SpiNNMachine
    1. sudo python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/spinnaker_tools.git
    1. git clone https://github.com/SpiNNakerManchester/spinn_common.git
    1. git clone https://github.com/SpiNNakerManchester/ybug.git
    1. git clone https://github.com/SpiNNakerManchester/Visualiser.git
    1. git clone https://github.com/SpiNNakerManchester/PyNNExamples.git
    1. sudo pip install enum34
    1. sudo pip install six
    1. sudo pip install pyNN
1. Continue to the [C Compiler Install](#CCOMPILE) to install the remaining c compiler dependency

# <a name="userGit"></a> User-Only gitclone

1. You now need to clone the github repositories for all the software stack. This requires you to run the following commands in a terminal, in the folder of your choice where the software will be installed.
    1. git clone https://github.com/SpiNNakerManchester/sPyNNaker.git
    1. cd sPyNNaker
    1. python setup.py develop --no-deps --user
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/sPyNNakerExtraModelsPlugin.git
    1. cd sPyNNakerExtraModelsPlugin
    1. python setup.py develop --no-deps --user
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git
    1. cd SpiNNFrontEndCommon
    1. python setup.py develop --no-deps --user
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/PACMAN.git
    1. cd PACMAN
    1. python setup.py develop --no-deps --user
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNMan.git
    1. cd SpiNNMan
    1. python setup.py develop --no-deps --user
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin.git
    1. cd sPyNNakerExternalDevicesPlugin
    1. python setup.py develop --no-deps --user
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/DataSpecification.git
    1. cd DataSpecification
    1. python setup.py develop --no-deps --user
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNMachine.git
    1. cd SpiNNMachine
    1. python setup.py develop --no-deps --user
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/spinnaker_tools.git
    1. git clone https://github.com/SpiNNakerManchester/spinn_common.git
    1. git clone https://github.com/SpiNNakerManchester/ybug.git
    1. git clone https://github.com/SpiNNakerManchester/Visualiser.git
    1. git clone https://github.com/SpiNNakerManchester/PyNNExamples.git
    1. pip install enum34 --user
    1. pip install six --user
    1. pip install pyNN --user
1. Continue to the [C Compiler Install](#CCOMPILE) to install the remaining c compiler dependency
 
# <a name="virtualGit"></a> Virtualenv git clone

These instructions will install the required packages only in a virtualenv.  Like the user-only installation, this can help when you don't have root access or are on a shared machine.  Additionally, it will help when you have several packages with conflicting dependencies, or those that occupy the same namespace (such as pyNN.spiNNaker if you have an older version of the toolchain).

If you already have installed sPyNNaker previously (and the optional sPyNNakerExtraDevicesPlugin and/or sPyNNakerExtraModelsPlugin), you will need to uninstall it:

1. Activate your virtualenv, ```<name>```  
```source <name>/bin/activate```
1. Uninstall the existing tools  
```pip uninstall pyNN-SpiNNaker```  
```pip uninstall sPyNNaker```  
```pip uninstall sPyNNakerExternalDevicesPlugin```  
```pip uninstall sPyNNakerExtraModelsPlugin```

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
1. go to [Virtual git clone](#virutal_git_clone) to complete the cloning of the git repositories

You can now [configure](#Configuration) your environment.

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
1. go to [Virtual git clone](#virutal_git_clone) to complete the cloning of the git repositories

You can now [configure](#Configuration) your environment.

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
1. go to [Virtual git clone](#virutal_git_clone) to complete the cloning of the git repositories

You can now [configure](#Configuration) your environment.

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
1. go to [Virtual git clone](#virutal_git_clone) to complete the cloning of the git repositories

You can now [configure](#Configuration) your environment.

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
1. go to [Virtual git clone](#virutal_git_clone) to complete the cloning of the git repositories

You can now [configure](#Configuration) your environment.

# <a name="virtual_git_clone"></a> Virtual git clone

1. You now need to clone the github repositories for all the software stack. This requires you to run the following commands in a terminal, in the folder of your choice where the software will be installed.
    1. git clone https://github.com/SpiNNakerManchester/sPyNNaker.git
    1. cd sPyNNaker
    1. python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/sPyNNakerExtraModelsPlugin.git
    1. cd sPyNNakerExtraModelsPlugin
    1. python setup.py develop --no-deps 
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git
    1. cd SpiNNFrontEndCommon
    1. python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/PACMAN.git
    1. cd PACMAN
    1. python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNMan.git
    1. cd SpiNNMan
    1. python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin.git
    1. cd sPyNNakerExternalDevicesPlugin
    1. python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/DataSpecification.git
    1. cd DataSpecification
    1. python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNMachine.git
    1. cd SpiNNMachine
    1. python setup.py develop --no-deps
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/spinnaker_tools.git
    1. git clone https://github.com/SpiNNakerManchester/spinn_common.git
    1. git clone https://github.com/SpiNNakerManchester/ybug.git
    1. git clone https://github.com/SpiNNakerManchester/Visualiser.git
    1. git clone https://github.com/SpiNNakerManchester/PyNNExamples.git
    1. pip install enum34
    1. pip install six
    1. pip install pyNN
1. Continue to the [C Compiler Install](#CCOMPILE) to install the remaining c compiler dependency

# <a name="CCOMPILE"></a> C Compiler Install
1. Primarily, you will need to install a C compiler that is compatible with SpiNNaker.  At present, we recommend using gcc for this.  Instructions for installing this on your system are below, depending on which platform you are using, as well as instructions for installing Perl, which is used by the development tools to modify the generated binaries to run on SpiNNaker:

* [Development Dependencies for 64-bit Ubuntu Linux](#Ubuntu64Dev)
 * [Development Dependencies for 64-bit Fedora Linux](#Fedora64Dev)
 * [Development Dependencies for 32-bit Ubuntu Linux](#Ubuntu32Dev)
 * [Development Dependencies for 32-bit Fedora Linux](#Fedora32Dev)
 * [Development Dependencies for Mac OS X](#MacOSXDev)
 * [Development Dependencies for Windows](#WindowsDev)

## <a name="Ubuntu64Dev"></a> Development Dependencies for 64-bit Ubuntu
1. Install 32-bit libc  
```sudo apt-get install libc6-i386```
1. Install perl and dependencies  
```sudo apt-get install perl perl-tk libterm-readline-gnu-perl```
1. Follow the instructions for the [Linux C Compiler](#LinuxC)

## <a name="Fedora64Dev"></a> Development Dependencies for 64-bit Fedora
1. Install 32-bit libc  
```sudo dnf install glibc.i686```
1. Install perl and dependencies  
```sudo dnf install perl perl-Tk perl-Term-ReadLine-Gnu```
1. Follow the instructions for the [Linux C Compiler](#LinuxC)

## <a name="Ubuntu32Dev"></a> Development Dependencies for 32-bit Ubuntu
1. Install perl and dependencies  
```sudo apt-get install perl perl-tk libterm-readline-gnu-perl```
1. Follow the instructions for the [Linux C Compiler](#LinuxC)

## <a name="Fedora32Dev"></a> Development Dependencies for 32-bit Fedora
1. Install perl and dependencies  
```sudo dnf install perl perl-Tk perl-Term-ReadLine-Gnu```
1. Follow the instructions for the [Linux C Compiler](#LinuxC)

## <a name="LinuxC"></a> Linux C Compiler
1. Download [CodeSourcery GCC ARM EABI Compiler](https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-lin-dev/arm-2013.05.tgz)
1. Extract the downloaded archive to the location of your choice
1. Add the "bin" directory within the installed location to the PATH environment variable in .profile in your home directory e.g. append the following:  
```export PATH=$PATH:<install-location>/bin```  
where ```<install-location>``` is the place where you extracted the file.

## <a name="MacOSXDev"></a> Development Dependencies for Mac OS X
1. Install the arm-none-eabi toolchain  
```sudo port install arm-none-eabi-gcc```
1. Install perl and dependencies  
```sudo port install perl5 p5-tk p5-term-readline-gnu```
1. *Optional:* Install Xcode and all its development tools from [here](https://developer.apple.com/xcode/downloads/) 
**NOTE:** take into account your Mac version.

## <a name="WindowsDev"></a> Development Dependencies for Windows
1. Download the prepackaged [MinGW Environment](https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win-dev/MinGW.zip)
1. Extract the downloaded archive to the location of your choice
1. Create a shortcut to MinGW/msys/1.0/msys.bat and add it to your start menu

You can now use the msys.bat to start up an environment from in which you can compile C code for SpiNNaker.

# <a name="SpinnakerTools"></a> SpiNNakerTools Installation
1. Create an environment variable ```SPINN_DIRS``` that points at the location of the cloned https://github.com/SpiNNakerManchester/spinnaker_tools.git (note that in Windows, this should be the MinGW Posix path e.g. if you have extracted the archive to C:\SpiNNaker-Tools\, you should set the environment variable to /c/SpiNNaker-Tools).
1. Run ```make``` in the root directory of the extracted archive.

# <a name="spinn_common"></a> spinn_common Library Installation
The spinn_common library will be installed into the SpiNNaker Tools installation directory, as set up above.

1. In the directory of the cloned https://github.com/SpiNNakerManchester/spinn_common.git, run ```make```.
1. Run ```make install```.

# <a name="SpinnFrontEndCommon"></a> SpiNNFrontEndCommon Library Installation
The SpiNNFrontEndCommon library will be installed into the SpiNNaker Tools installation directory, as set up above.

1. In the ```c_common``` directory of the cloned https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git, run ```make```.
1. Run ```make install```.

# <a name="Ybug"></a> YBug Installation

If you want to avoid having to run "source setup" in the ybug folder every time you log in or start a new terminal:

1. Add the cloned ybug folder to your ```PATH``` environment variable
1. Add the cloned ybug folder to your ```PERL5LIB``` environment variable (or create this environment variable if it is not already set; note that in Windows, this should be the MinGW Posix path e.g. if you have extracted the archive to C:\ybug\, you should set the environment variable to /c/ybug)
1. If you are going to boot your board using ybug, create a new environment variable ```YBUG_PATH``` and set this to the ```boot``` subdirectory of the extracted ybug folder.

To run ybug:

1. If you haven't added the environment variables detailed above, go into the directory where you extracted the archive and run:  
```source setup```
1. Run:  
```ybug <ip-or-host>```  
where ```<ip-or-host>``` is the ip address or hostname of your SpiNNaker board.
1. Type ```help``` to get further usage instructions.

# <a name="BuildUsage"></a> Build System Usage

When using the make-files supplied in this repository, you must set up a number
of environment variables using:

	$ cd spinnaker_tools  # You must be in the spinnaker_tools directory!
	$ source setup

You should also ensure you have compiled the SpiNNaker libraries as described
above otherwise application compilation will fail.

## <a name="Compilation"></a> Basic Application Compilation

To quickly compile a simple single-file application for SpiNNaker, you can use the following command:

	$ make -f $SPINN_DIRS/Makefile.app APP=example

This will compile the application in `example.c` and produce a SpiNNaker binary called `example.aplx` in the current directory.

## <a name="Makefile"></a> Example Makefile

Though the above is suitable while prototyping applications, real-world applications may contain many source files and should be compiled using their own makefile.

`Makefile.example` in the root of the `spinnaker_tools` repository provides an annotated Makefile template which compiles simple C programs for SpiNNaker using these tools. Once your makefile is set up, your application can then be compiled by calling:

	$ make


1. Continue to the [Compile Binaries](#CCOMPILEBINARIES) to complete the installation by compiling the binaries of the c code used by the tool chain.

## <a name="CCOMPILEBINARIES"></a> Compile Binaries

1. to compile the c code used by the tool chain, either:

1. run this script [automatic_make_spynnaker.sh](../documents/automatic_make_spynnaker.sh)
1. run the following instructions from the base folder where all the software is installed:

    1. cd spinnaker_tools
    1. source setup
    1. cd ..
    1. cd spinn_common
    1. make clean
    1. make 
    1. make install
    1. cd ..
    1. cd SpiNNMan/c_models/reinjector/
    1. make 
    1. cd ../../..
    1. cd SpiNNFrontEndCommon/c_common/front_end_common_lib/
    1. make install-clean
    1. cd ..
    1. make clean
    1. make 
    1. make install
    1. cd ../..
    1. cd sPyNNaker/neural_modelling/
    1. make clean
    1. make 
    1. source setup
    1. cd sPyNNakerExternalDevicesPlugin/neural_modelling/
    1. make clean
    1. make 
    
    
1. Continue to [configure](#Configuration) your environment.

# <a name="Configuration"></a> Configuration
When SpyNNaker is first called, if a configuration file is not found, it will create one in your home directory and exit.  It is possible to ask SpyNNaker to do this before you run your first simulation as follows:  
```python -c "import pyNN.spiNNaker"```

Note that if you have previously installed a version of the spiNNaker software, you may already have a file called ".pacman.cfg" in your home directory.  In this case, SpyNNaker will attempt to use this file for its parameters.  If you don't have this file, a new file called ".spynnaker.cfg" will be created in your home directory.  You must edit this file to ensure that SpyNNaker can access your SpiNNaker machine.  Upon opening this file, the part to alter will look like the following:  
```[Machine] ```  
```machineName = None ```  
```version = None ```

Within the file, you should set ```machineName``` to the IP address or hostname of your SpiNNaker machine, and ```version``` to the version of your SpiNNaker board; this will almost certainly be "3" for a 4-chip board or "5" on a 48-chip board.

The default ip address for a spinn-3 board is 192.168.240.253 and the default ip address for a spinn-5 board is 192.168.240.1

# <a name="Network Configuration"></a> Network Configuration

1. Go to your network settings and add a IPv4 entry with the following address to your wired settings:  
    1. ip address = 192.168.240.254
    2. sub mask = 255.255.255.0
    3. default gateway = 0.0.0.0

# <a name="Examples"></a> Running some examples
1. Download the examples from [here](https://github.com/SpiNNakerManchester/PyNNExamples/archive/2016.001.zip) (zip) or [here](https://github.com/SpiNNakerManchester/PyNNExamples/archive/2016.001.tar.gz) (tar.gz)
1. Extract the archive
1. Go to the "examples" folder
1. Run:  
```python va_benchmark.py```
1. You will see the system go through a series of processes from partitioning, to placement, to routing and finally to loading and running.
1. Once the example has finished, you should see a graph, that will look something like this:  
![VABenchmarkSpikes](va_benchmark.png)
If you get the output above, you have successfully installed your system.

# Helpful documents

Depending upon what the developer is planning to work on, one or more pages covered in [Developer tutorial](../common_pages/developer_tutorial.html) may be usful to read. 

# <a name="Trouble"></a> Troubleshooting

1. If you experience the error:

```**UnicodeDecodeError: 'ascii' codec can't decode byte 0xb0 in position 1: ordinal not in range(128)**``` 

Then to solve it, edit C:\Python27\Lib\mimetypes.py and add these codes:

    if sys.getdefaultencoding() != 'gbk':  
        reload(sys)
        sys.setdefaultencoding('gbk')
 
before the following line:

    default_encoding = sys.getdefaultencoding()
