---
title: spinnaker_tools
---

spinnaker_tools contains all the requirements for building C binaries for execution on SpiNNaker, as well as the SpiNNaker boot and monitor processor code.  This includes:

 * SC&MP, the SpiNNaker low-level boot and monitor process.
 * SARK, the SpiNNaker low-level C library.
 * Spin1 API, the SpiNNaker low-level hardware abstraction API.
 * ybug, for low-level execution of binaries and debugging.
 * tools and Makefiles, for constructing executables to be run on SpiNNaker.
 
# Installation

1. [Install Development Dependencies](#DevelopmentDependencies)
1. [Install Spinnaker Tools](#SpinnakerTools)

Once you've got a working development environment:

* [`spinnaker_tools` Build System Usage](#BuildUsage)
  * [Compiling simple, one-off, single-C-file applications](#Compilation)
  * [Creating a Makefile for SpiNNaker C projects](#Makefile)

# <a name="DevelopmentDependencies"></a> Install Development Dependencies
Primarily, you will need to install a C compiler that is compatible with SpiNNaker.  At present, we recommend using gcc for this.  Instructions for installing this on your system are below, depending on which platform you are using, as well as instructions for installing Perl, which is used by the development tools to modify the generated binaries to run on SpiNNaker:

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
1. Download the current version of SpiNNaker Tools from [here](https://github.com/SpiNNakerManchester/spinnaker_tools/releases/download/v3.0.1/spinnaker_tools_3.0.1.tar.gz)
1. Extract the archive to the location of your choice.
1. Create an environment variable ```SPINN_DIRS``` that points at the location of the extracted archive (note that in Windows, this should be the MinGW Posix path e.g. if you have extracted the archive to C:\spinnaker_tools\, you should set the environment variable to /c/spinnaker_tools).
1. Add the tools folder in the extracted archive to your ```PATH``` environment variable.  This does not need to be a POSIX path on Windows e.g. C:\spinnaker_tools\tools is fine on Windows, or /spinnaker_tools/tools on Linux or Mac.
1. Add the extracted tools folder to your ```PERL5LIB``` environment variable (or create this environment variable if it is not already set; note that in Windows, this should be the MinGW Posix path e.g. if you have extracted the archive to C:\spinnaker_tools\, you should set the environment variable to /c/spinnaker_tools/tools).
1. Run ```make``` in the root directory of the extracted archive.

# <a name="BuildUsage"></a> Build System Usage

When using the makefiles supplied in this repository, you must set up a number
of environment variables using:

	$ cd spinnaker_tools  # You must be in the spinnaker_tools directory!
	$ source setup

You should also ensure you have compiled the SpiNNaker libraries as described
above otherwise application compilation will fail.

## <a name="Compilation"></a> Basic Application Compilation

To quickly compile a simple single-file application for SpiNNaker, you can use the following command:

	$ make -f $SPINN_DIRS/make/app.make APP=example

This will compile the application in `example.c` and produce a SpiNNaker binary called `example.aplx` in the current directory.

## <a name="Makefile"></a> Example Makefile

Though the above is suitable while prototyping applications, real-world applications may contain many source files and should be compiled using their own makefile.  A number of example applications are provided in the `apps` folder to show you how this is done.
