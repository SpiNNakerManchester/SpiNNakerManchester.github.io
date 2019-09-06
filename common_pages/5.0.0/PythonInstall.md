---
title: Python Dependencies for SpiNNaker
---

This guide will detail how to install the core Python dependencies for SpiNNaker.

This has been tested using Fedora Linux 20 64-bit, Ubuntu Linux 14.04 LTS 64-bit, Ubuntu Linux 16.04 LTS 64-bit, Windows 8.1 64-bit, Mac OS X Mavericks and Mac OS X Yosemite, but it should in principle work on 32-bit and 64-bit versions of Fedora and Ubuntu Linux, Windows 7, 8 and 10, and Mac OS X.

* [Ubuntu Linux Requirements](#UbuntuPython)
* [Fedora Linux Requirements](#FedoraPython)
* [Mac OS X Requirements](#MacOSXPython)
* [Windows Requirements](#WindowsPython)
* [Windows PATH settings](#WindowsPath)

# Linux

## <a name="UbuntuPython"></a> Ubuntu Linux Requirements
1. If you are on Ubuntu 16 or less, you will need to add a repository to get later versions of Python

       sudo add-apt-repository ppa:jonathonf/python-3.6
       sudo apt-get update

1. Install Python

       sudo apt-get install python3.6

1. Upgrade pip and dependencies

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

       sudo port install python36
       sudo port select --set python python36
       sudo port select --set pip pip36

1. Upgrade pip and dependencies

       sudo pip install --upgrade pip setuptools wheel

# <a name="WindowsPython"></a>Windows

Note that you need to install the correct build of the tools _and_ update your `PATH` environment variable for the toolchain to work.

Users with an up-to-date version of Windows 10 64-bit may want to use the [Linux Subsystem for Windows 10](https://msdn.microsoft.com/en-gb/commandline/wsl/install_guide?f=255&MSPPError=-2147217396).  This has been tested with an Ubuntu 14.04 install and seems to work well.
For graphics content, you will also need to install and run [an X-Windows Server](https://sourceforge.net/projects/xming/).
After installing, you should follow the [Ubuntu installation instructions](#UbuntuPython) and __not__ the instructions below.

1. Download and install [Python 3.6](https://www.python.org/downloads/).

1. Download and install [setuptools](https://github.com/SpiNNakerManchester/github.SpiNNakerManchester.io/releases/download/v1.0-win64/setuptools-5.8.win-amd64-py2.7.exe).

1. Update pip and dependencies - from an administrative console, run:

       pip install --upgrade pip setuptools wheel

Continue to [edit your PATH](#WindowsPath).

## <a name="WindowsPath"></a> Windows Path Settings
Edit your PATH environment variable to include the `Python27`, `Python27\Scripts` and (if installed) `gtk\bin` directories.
  1. Go to "Control Panel"
  1. Go to "System" (may be under "System and Security")
  1. Select "Advanced System Settings"
  1. Select "Environment Variables"
  1. Select the "Path" in the "System Variables" box at the bottom
  1. Click on "Edit"
  1. Add the new directory by putting it before the existing string, followed by a single semi-colon; for example, if you installed the dependencies to the default/recommended locations, prepend `Path` with:

         C:\Python27;C:\Python27\Scripts;
