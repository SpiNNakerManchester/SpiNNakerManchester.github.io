---
title: C Compiler for SpiNNaker
---
To build programs on SpiNNaker, you will primarily need to install a C compiler that is compatible with SpiNNaker.  At present, we recommend using gcc for this.  Instructions for installing this on your system are below, depending on which platform you are using, as well as instructions for installing Perl, which is used by the development tools to modify the generated binaries to run on SpiNNaker:

 * [Development Dependencies for 64-bit Ubuntu Linux](#Ubuntu64Dev)
 * [Development Dependencies for 64-bit Fedora Linux](#Fedora64Dev)
 * [Development Dependencies for 32-bit Ubuntu Linux](#Ubuntu32Dev)
 * [Development Dependencies for 32-bit Fedora Linux](#Fedora32Dev)
 * [Development Dependencies for Mac OS X](#MacOSXDev)
 * [Development Dependencies for Windows](#WindowsDev)

# Linux

## <a name="Ubuntu64Dev"></a> Development Dependencies for 64-bit Ubuntu

1. Install 32-bit libc

       sudo apt-get install libc6-i386

1. Install perl and dependencies

       sudo apt-get install perl perl-tk libterm-readline-gnu-perl

1. Follow the instructions for the [Linux C Compiler](#LinuxC), below.

## <a name="Fedora64Dev"></a> Development Dependencies for 64-bit Fedora

1. Install 32-bit libc

       sudo dnf install glibc.i686

1. Install perl and dependencies

       sudo dnf install perl perl-Tk perl-Term-ReadLine-Gnu

1. Follow the instructions for the [Linux C Compiler](#LinuxC), below.

## <a name="Ubuntu32Dev"></a> Development Dependencies for 32-bit Ubuntu

1. Install perl and dependencies

       sudo apt-get install perl perl-tk libterm-readline-gnu-perl

1. Follow the instructions for the [Linux C Compiler](#LinuxC), below.

## <a name="Fedora32Dev"></a> Development Dependencies for 32-bit Fedora

1. Install perl and dependencies

       sudo dnf install perl perl-Tk perl-Term-ReadLine-Gnu

1. Follow the instructions for the [Linux C Compiler](#LinuxC), below.

## <a name="LinuxC"></a> Linux C Compiler

1. Download [GCC ARM NONE EABI Compiler](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads/6-2017-q2-update).
Note Windows users pick the "Linux 64-bit" as it will be used inside the shell.

1. Extract the downloaded archive to the location of your choice

1. Add the "bin" directory within the installed location to the PATH environment variable in `.profile` in your home directory, e.g., append the following:

       export PATH=$PATH:<install-location>/bin

   where `<install-location>` is the place where you extracted the file.

# Mac OS X

## <a name="MacOSXDev"></a> Development Dependencies for Mac OS X

1. If you haven't done so already, install Xcode and all its development tools from [here](https://developer.apple.com/xcode/downloads/) or via the App Store. **NOTE:** take into account your Mac version if using a direct download.

1. If you haven't done so already, sign the Xcode license to enable compilation on your computer.

       sudo xcodebuild -license

1. If you haven't done so already, install [Mac Ports](https://www.macports.org/install.php).

1. Install the arm-none-eabi toolchain.

       sudo port install arm-none-eabi-gcc

1. Install perl and related dependencies.

       sudo port install perl5 p5-tk p5-term-readline-gnu

# Windows

## <a name="WindowsDev"></a> Development Dependencies for Windows

Users with an up-to-date version of Windows 10 64-bit may want to use the [Linux Subsystem for Windows 10](https://msdn.microsoft.com/en-gb/commandline/wsl/install_guide?f=255&MSPPError=-2147217396).  This has been tested with an Ubuntu 14.04 install and seems to work well.
For graphics content, you will also need to install and run [an X-Windows Server](https://sourceforge.net/projects/xming/).
After installing, you should follow the [Ubuntu installation instructions](#Ubuntu64Dev).

All other Windows Users should follow the instructions below.

1. Download the prepackaged [MinGW Environment](https://github.com/SpiNNakerManchester/SpiNNakerManchester.github.io/releases/download/v1.0-win-dev/MinGW.zip).
1. Extract the downloaded archive to the location of your choice
1. Create a shortcut to `MinGW/msys/1.0/msys.bat` and add it to your start menu

You can now use the `msys.bat` to start up an environment from in which you can compile C code for SpiNNaker.

Note the make requires access to the python package spinn_utilities.make_tools.
This requires inside the Ubuntu/minGW window
- sudo apt-get update
- sudo apt install python
- sudo pip install setuptools
- Change to the directory with SpiNNakerManchester/SpiNNUtils
- sudo python setup.py develop
