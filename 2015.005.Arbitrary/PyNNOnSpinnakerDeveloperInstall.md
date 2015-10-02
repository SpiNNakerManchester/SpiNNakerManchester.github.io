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
```sudo yum install python```
1. Install numpy  
```sudo yum install numpy```
1. Install scipy  
```sudo yum install scipy```
1. Install lxml  
```sudo yum install python-lxml```
1. Install pip  
```sudo yum install python-pip```
1. *Optional:* Install matplotlib (often used in PyNN scripts for plotting graphs)  
```sudo yum install python-matplotlib```

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

1. You now need to clone the github resposorities for all the software stack. This requires you to run the following commands in a terminal, in the folder of your choice where the software will be installed.
    1. git clone https://github.com/SpiNNakerManchester/sPyNNaker.git
    1. cd sPyNNaker
    1. python setup.py develops
    1. cd ..
    1. git cline https://github.com/SpiNNakerManchester/sPyNNakerExtraModelsPlugin.git
    1. cd sPyNNakerExtraModelsPlugin
    1. python setup.py develops
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git
    1. cd SpiNNFrontEndCommon
    1. python setup.py develops
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/PACMAN.git
    1. cd PACMAN
    1. python setup.py develops
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNMan.git
    1. cd SpiNNMan
    1. python setup.py develops
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin.git
    1. cd sPyNNakerExternalDevicesPlugin
    1. python setup.py develops
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/DataSpecification.git
    1. cd DataSpecification
    1. python setup.py develops
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNMachine.git
    1. cd SpiNNMachine
    1. python setup.py develops
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/SpiNNakerGraphFrontEnd.git
    1. cd SpiNNakerGraphFrontEnd
    1. python setup.py develops
    1. cd ..
    1. git clone https://github.com/SpiNNakerManchester/spinnaker_tools.git
    1. git clone https://github.com/SpiNNakerManchester/spinn_common.git
    1. git clone https://github.com/SpiNNakerManchester/ybug.git
    1. git clone https://github.com/SpiNNakerManchester/Visualiser.git
    1. git clone https://github.com/SpiNNakerManchester/PyNNExamples.git
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
```sudo yum install glibc.i686```
1. Install perl and dependencies  
```sudo yum install perl perl-Tk perl-Term-ReadLine-Gnu```
1. Follow the instructions for the [Linux C Compiler](#LinuxC)

## <a name="Ubuntu32Dev"></a> Development Dependencies for 32-bit Ubuntu
1. Install perl and dependencies  
```sudo apt-get install perl perl-tk libterm-readline-gnu-perl```
1. Follow the instructions for the [Linux C Compiler](#LinuxC)

## <a name="Fedora32Dev"></a> Development Dependencies for 32-bit Fedora
1. Install perl and dependencies  
```sudo yum install perl perl-Tk perl-Term-ReadLine-Gnu```
1. Follow the instructions for the [Linux C Compiler](#LinuxC)

## <a name="LinuxC"></a> Linux C Compiler
1. Download [CodeSourcery GCC ARM EABI Compiler](https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-lin-dev/arm-2013.05.tgz)
1. Extract the downloaded archive to the location of your choice
1. Add the "bin" directory within the installed location to the PATH enviroment variable in .profile in your home directory e.g. append the following:  
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

When using the makefiles supplied in this repository, you must set up a number
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


1. Continue to the [Compile Binaries](#CCOMPILEBINARIES) to compelte the installation by compiling the binaries of the c code used by the tool chain.

## <a name="CCOMPILEBINARIES"></a> Compile Binaries

1. to compile the c code used by the tool chain, run the following instructions from the base folder where all the software is installed:
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
    1. cd ../../SpiNNakerGraphFrontEnd/examples/
    1. make clean
    1. make 
    
1. Continue to [configure](#Configuration) your environment.

# <a name="Configuration"></a> Configuration
When SpyNNaker is first called, if a configuration file is not found, it will create one in your home directory and exit.  It is possible to ask SpyNNaker to do this before you run your first simulation as follows:  
```python -c "import pyNN.spiNNaker"```

Note that if you have previously installed a version of the spiNNaker software, you may already have a file called ".pacman.cfg" in your home directory.  In this case, SpyNNaker will attempt to use this file for its paramters.  If you don't have this file, a new file called ".spynnaker.cfg" will be created in your home directory.  You must edit this file to ensure that SpyNNaker can access your SpiNNaker machine.  Upon opening this file, the part to alter will look like the following:  
```[Machine] ```  
```machineName = None ```  
```version = None ```

Within the file, you should set ```machineName``` to the IP address or hostname of your SpiNNaker machine, and ```version``` to the version of your SpiNNaker board; this will almost certainly be "3" for a 4-chip board or "5" on a 48-chip board.

# <a name="Examples"></a> Running some examples
1. Download the examples from [here](https://github.com/SpiNNakerManchester/PyNNExamples/archive/2015.003.01.zip) (zip) or [here](https://github.com/SpiNNakerManchester/PyNNExamples/archive/2015.003.01.tar.gz) (tar.gz)
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
