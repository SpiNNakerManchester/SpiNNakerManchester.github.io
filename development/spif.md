---
title: Using spif with sPyNNaker
---

The spif interface is connected to an FPGA on SpiNNaker and allows high-bandwidth input from spiking retina devices.  It is assumed that it is connected to FPGA 0 via the J5 SATA connector on a 48-node board.  It is possible to connect multiple spif interfaces on a multi-board system; the ID of the Ethernet chip on the board that each interface is connected to must be known.  Note that the SpiNNaker board FPGAs may also need to be updated with the latest firmware for this to work.

The SpiNNaker software current supports spif on the extdev_fpgas branches of the git repositories.  These can be used by following the instructions [here](gitinstall.html) and then switching the following branches to extdev_fpgas (e.g. ``cd <module>; git checkout extdev_fpgas``):

 - SpiNNMachine
 - PACMAN
 - SpiNNFrontEndCommon
 - sPyNNaker
 - JavaSpiNNaker (optional: only if you have use_java=True in your config file)

Once the branches are on the correct version of the software run the following:

 - ``SupportScripts/automatic_make.sh``
 - ``mvn -f JavaSpiNNaker -DskipTests=True clean package``
    
Once the software is up-to-date, the spif board can be used with a retina device using the external device ``p.external_devices.SPIFRetinaDevice``, which has the following arguments:

    SPIFRetinaDevice(pipe, width, height, sub_width, sub_height,
                 base_key=None, input_x_shift=16, input_y_shift=0,
                 board_address=None, chip_coords=None)

where:
    
 - ``pipe``: The index of the pipe to use on the board (0 or 1).  Pipe 0 uses UDP port 3333 and Pipe 1 uses UDP port 3334; note that connecting a USB device will use Pipe 0 initially and disable UDP input on that pipe.  Connecting a second USB device will then also override UDP input on Pipe 1.  When two USB devices are connected, the Pipe to which a USB device is connected to depends on the ID of the device; the device with the lowest ID will connect to Pipe 0 and the device with the highest ID will connect to Pipe 1.
 - ``width, height``: The width and height, in pixels, of the device.
 - ``sub_width, sub_height``: The width and height of a sub-rectangle to split the device input into.  This allows the output from different parts of the device to be received by different cores, avoiding the need for every core to receive every pixel and so reducing the traffic that each core needs to handle.  The effectiveness of the sub-rectangle depends on the connectivity between the device and the receiving cores.  Note that too small a rectangle may result in too many additional routing entries being created, which then might not fit on the SpiNNaker machine.
 - ``base_key``: The key to use for the top bits in each spike to be sent by the retina.  This is optional; if not specified, it will use key 0 for first device, 1 for the second and so on.
 - ``input_x_shift, input_y_shift``: The shift that spif should apply to the received values to obtain the x and y coordinates.
 - ``board_address``: The IP address of the board to which spif is connected.  Optional if there is only one board, or spif is connected to the boot board, or chip_coords are specified instead.
 - ``chip_coords``: The coordinates of the Ethernet chip of a multi-board machine to which spif is connected.  Optional if there is only one board, or spif is connected to the boot board, or board_address is specified instead.  If chip_coords and board_address are both specified, chip_coords will be used first with board_address then used if chip_coords don't connect to an FPGA.
    
This branch also contains work on [2D convolutions](2d_convolutions).
