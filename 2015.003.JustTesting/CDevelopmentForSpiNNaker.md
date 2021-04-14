---
title: C Development for SpiNNaker
---

# The version described here is no longer supported. 

[Home page for current version](/) 

This guide is intended to help you set up your development environment so that you can write C code and compile binaries to be run on SpiNNaker.


# Contents

1. [Install Development Dependencies](#DevelopmentDependencies)
1. [Install Spinnaker Tools](#SpinnakerTools)
1. *Optional*: [Install spinn_common Library](#spinn_common) (for additional utility, mathematical and efficiency library functions)
1. *Optional*: [Install ybug](#Ybug) (for command-line debugging)


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

## <a name="WindowsDev"></a> Development Dependencies for Windows
1. Download the prepackaged [MinGW Environment](https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win-dev/MinGW.zip)
1. Extract the downloaded archive to the location of your choice
1. Create a shortcut to MinGW/msys/1.0/msys.bat and add it to your start menu

You can now use the msys.bat to start up an environment from in which you can compile C code for SpiNNaker.

# <a name="SpinnakerTools"></a> SpiNNakerTools Installation
1. Download the current version of SpiNNaker Tools [as a zip](https://github.com/SpiNNakerManchester/spinnaker_tools/archive/2015.001.zip) or [as a tar.gz](https://github.com/SpiNNakerManchester/spinnaker_tools/archive/2015.001.tar.gz)
1. Extract the archive to the location of your choice.
1. Create an environment variable ```SPINN_DIRS``` that points at the location of the extracted archive (note that in Windows, this should be the MinGW Posix path e.g. if you have extracted the archive to C:\SpiNNaker-Tools\, you should set the environment variable to /c/SpiNNaker-Tools).
1. Run ```make``` in the root directory of the extracted archive.

# <a name="spinn_common"></a> spinn_common Library Installation
The spinn_common library will be installed into the SpiNNaker Tools installation directory, as set up above.

1. Download the current version of spinn_common [as a zip](https://github.com/SpiNNakerManchester/spinn_common/archive/2015.001.zip) or [as a tar.gz](https://github.com/SpiNNakerManchester/spinn_common/archive/2015.001.tar.gz).
1. Extract the archive to the location of your choice.
1. In the directory of the extracted archive, run ```make```.
1. Run ```make install```.

# <a name="Ybug"></a> YBug Installation
1. Download the current version of ybug [as a zip](https://github.com/SpiNNakerManchester/ybug/archive/2015.001.zip) or [as a tar.gz](https://github.com/SpiNNakerManchester/ybug/archive/2015.001.tar.gz).
1. Extract the archive to the location of your choice.

If you want to avoid having to run "source setup" in the ybug folder every time you log in or start a new terminal:

1. Add the extracted ybug folder to your ```PATH``` environment variable
1. Add the extracted ybug folder to your ```PERL5LIB``` environment variable (or create this environment variable if it is not already set)
1. If you are going to boot your board using ybug, create a new environment variable ```YBUG_PATH``` and set this to the ```boot``` subdirectory of the extracted ybug folder.

To run ybug:

1. If you haven't added the environment variables detailed above, go into the directory where you extracted the archive and run:  
```source setup```
1. Run:  
```ybug <ip-or-host>```  
where ```<ip-or-host>``` is the ip address or hostname of your SpiNNaker board.
1. Type ```help``` to get further usage instructions.
