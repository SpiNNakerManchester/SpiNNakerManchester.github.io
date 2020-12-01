---
title: High-level C development for SpiNNaker
---

This guide will help you to install the tools required for development with the high-level software for SpiNNaker, including sPyNNaker and SpiNNakerGraphFrontEnd.

The steps required are:

1. [Install a compiler and spinnaker_tools](/spinn_tools/3.1.0/)
1. [Install spinn_common Library](#spinn_common) (for additional utility, mathematical and efficiency library functions)
1. [Install SpiNNFrontEndCommon Library](#SpinnFrontEndCommon) (for front-end development support)

# <a name="spinn_common"></a> spinn_common Library Installation
The spinn_common library will be installed into the SpiNNaker Tools installation directory, as set up above.

1. Download the current version of spinn_common [as a zip](https://github.com/SpiNNakerManchester/spinn_common/archive/3.0.0.zip) or [as a tar.gz](https://github.com/SpiNNakerManchester/spinn_common/archive/3.0.0.tar.gz).
1. Extract the archive to the location of your choice.
1. In the directory of the extracted archive, run ```make```.
1. Run ```make install```.

# <a name="SpinnFrontEndCommon"></a> SpiNNFrontEndCommon Library Installation
The SpiNNFrontEndCommon library will be installed into the SpiNNaker Tools installation directory, as set up above.

1. Download the current version of SpiNNFrontEndCommon [as a zip](https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/archive/3.0.0.zip) or [as a tar.gz](https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/archive/3.0.0.tar.gz).
1. Extract the archive to the location of your choice.
1. In the ```c_common``` directory of the extracted archive, run ```make```.
1. Run ```make install```.
