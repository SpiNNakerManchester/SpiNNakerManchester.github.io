---
title: C Compiler for SpiNNaker
---
# The version described here is no longer supported. 

[Home page for current version](/) 

To build programs on SpiNNaker, you will primarily need to install a C compiler that is compatible with SpiNNaker.  At present, we recommend using gcc for this.  Instructions for installing this on your system are below, depending on which platform you are using, as well as instructions for installing Perl, which is used by the development tools to modify the generated binaries to run on SpiNNaker:

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
1. Download [GCC ARM EABI Compiler](https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q3-update/+download/gcc-arm-none-eabi-5_4-2016q3-20160926-linux.tar.bz2)
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