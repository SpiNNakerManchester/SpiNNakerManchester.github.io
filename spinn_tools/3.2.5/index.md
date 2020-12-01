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

1. [Install Development Dependencies](/common_pages/5.0.0/Compiler.html)
1. [Install Spinnaker Tools](#SpinnakerTools)

Once you've got a working development environment:

 * [`spinnaker_tools` Build System Usage](#BuildUsage)
 * [Compiling simple, one-off, single-C-file applications](#Compilation)
 * [Creating a Makefile for SpiNNaker C projects](#Makefile)

# <a name="SpinnakerTools"></a> SpiNNakerTools Installation
1. Download the current version of SpiNNaker Tools from [here](https://github.com/SpiNNakerManchester/spinnaker_tools/releases/download/v3.2.5/spinnaker_tools_3.2.5.tar.gz)
1. Extract the archive to the location of your choice.
1. Create an environment variable `SPINN_DIRS` that points at the location of the extracted archive (note that in Windows, this should be the MinGW Posix path e.g. if you have extracted the archive to `C:\spinnaker_tools\`, you should set the environment variable to `/c/spinnaker_tools`).
1. Add the tools folder in the extracted archive to your `PATH` environment variable.  This does not need to be a POSIX path on Windows e.g. `C:\spinnaker_tools\tools` is fine on Windows, or `/spinnaker_tools/tools` on Linux or Mac.
1. Add the extracted tools folder to your `PERL5LIB` environment variable (or create this environment variable if it is not already set; note that in Windows, this should be the MinGW Posix path, e.g., if you have extracted the archive to `C:\spinnaker_tools\`, you should set the environment variable to `/c/spinnaker_tools/tools`).
1. Run `make` in the root directory of the extracted archive.

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
