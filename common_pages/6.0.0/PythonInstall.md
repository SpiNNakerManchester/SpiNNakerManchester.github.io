---
title: Python Dependencies for SpiNNaker
---

This guide will detail how to install the core Python dependencies for SpiNNaker.

This has been tested using Ubuntu Linux 14.04 LTS 64-bit, Ubuntu Linux 16.04 LTS 64-bit, Ubuntu Linux 18.04 LTS 64-bit, Windows 10 64-bit and Mac OS X but it should in principle work on 32-bit and 64-bit versions of Fedora and Ubuntu Linux, Windows 7, 8 and 10, and Mac OS X.

Note that once you have completed these instructions, the remainder of the installation instructions assume that the command "python" points at the version of Python you have installed here; please ensure that this is the case.

* [Ubuntu Linux Requirements](#UbuntuPython)
* [Fedora Linux Requirements](#FedoraPython)
* [Mac OS X Requirements](#MacOSXPython)
* [Windows Requirements](#WindowsPython)
* [Windows PATH settings](#WindowsPath)

# Linux

## <a name="UbuntuPython"></a> Ubuntu Linux Requirements
1. If you are on Ubuntu 16 or less, you will need to add a repository to get later versions of Python

       sudo add-apt-repository ppa:deadsnakes/ppa
       sudo apt-get update

1. Install Python

       sudo apt-get install python3.8

1. Upgrade pip and dependencies (be careful at this point that the version of pip you use here is the Python 3 version; you may need to type "pip3" instead of "pip")

       sudo pip install --upgrade pip setuptools wheel

## <a name="FedoraPython"></a> Fedora Linux Requirements

1. Install Python

       sudo dnf install python

1. Upgrade pip and dependencies

       sudo pip install --upgrade pip setuptools wheel

# Mac OS X

## <a name="MacOSXPython"></a> Mac OS X Requirements

1. Download and install <a href="https://www.macports.org/install.php" target="_blank">MacPorts</a> (Requires [XCode](https://developer.apple.com/technologies/tools/) Developer Tools and an X11 windowing environment such as [XQuartz](https://www.xquartz.org/)). Note that with some versions of OS X, you might need to [accept the Xcode license](https://apple.stackexchange.com/questions/175069/how-to-accept-xcode-license) if you haven't already done so.

1. Install python

       sudo port install python38
       sudo port select --set python python38
       sudo port select --set pip pip38

1. Upgrade pip and dependencies

       sudo pip install --upgrade pip setuptools wheel

# <a name="WindowsPython"></a>Windows

Note that you need to install the correct build of the tools _and_ update your `PATH` environment variable for the toolchain to work.

Users with an up-to-date version of Windows 10 64-bit may want to use the [Linux Subsystem for Windows 10](https://msdn.microsoft.com/en-gb/commandline/wsl/install_guide?f=255&MSPPError=-2147217396).  This has been tested with an Ubuntu 14.04 install and seems to work well.
For graphics content, you will also need to install and run [an X-Windows Server](https://sourceforge.net/projects/xming/).
After installing, you should follow the [Ubuntu installation instructions](#UbuntuPython) and __not__ the instructions below.

1. Download and install [Python 3.8](https://www.python.org/downloads/).  It is advised
to install in a location without spaces e.g. C:\Python38.

1. Update pip and dependencies - from an administrative console, run:

       pip install --upgrade pip setuptools wheel
