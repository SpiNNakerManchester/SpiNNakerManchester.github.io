---
title: Extracting data from a simulation on a SpiNNaker machine in real time
---
# The version described here is no longer supported. 

[Home page for current version](/) 

This page describes how to use the SpiNNaker tool chain to support real time data extraction from an application running on a SpiNNaker machine.

# Page Contents
* [Installation Instructions](#installation)
* [Ethos and Disclaimer](#ethos)
* [How real Time output works] (#outputdef)
* [Constraints] (#constraints)
* [PyNN setting up for live output](#liveoutput)
* [Python Based Reciever](#python_based) 
* [C Based Reciever](#c_based)
* [Troubleshooting](#trouble)


# <a name="installation"></a> Installation Instructions

To support a live stream of data from a SpiNNaker machine, requires installation of the 
[**sPyNNakerExternalDevicesPlugin**](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007)  which requires the end user to **open a terminal / cmd prompt** and run the command:

```pip install sPyNNakerExternalDevicesPlugin```

This now allows the sPyNNakerExternalDevicesPlugin module to be imported to your PyNN script though the command:

```import spynnaker_external_devices_plugin.pyNN as externaldevices```


# <a name="ethos"></a> Ethos and Disclaimer

The ethos between [sPyNNaker](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.003) and [sPyNNakerExternalDevicesPlugin](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007) modules is that the [sPyNNaker](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.003) module contains functionality which is supported by the PyNN language. Functionality which goes beyond the PyNN language is supported via plug-ins, and for this topic the functionality is supported in the  [sPyNNakerExternalDevicesPlugin](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007).

The rest of this page walks through how to use the Live_packet_gather model via two scripts stored inside the [PyNNExamples](https://github.com/SpiNNakerManchester/PyNNExamples/tree/f742b9816e402558fe23bde31e8abcb266e709b5/) module under the [/receiving_scripts](https://github.com/SpiNNakerManchester/PyNNExamples/tree/f742b9816e402558fe23bde31e8abcb266e709b5/examples/external_device_examples/injection_scripts) folder.

# <a name="outputdef"></a> How real time output works 

This section describes how the tool chain infrastructure works within the SpiNNaker machine. Below is a diagram which describes how packets from a collection of cores, been programmed to transmit packets outside the SpiNNaker machine, via the ethernet, are routed. Packets transmitted from cores are not directly transmitted outside the SpiNNaker machine; Instead these packets are relayed to a [LivePacketGather](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007/spynnaker_external_devices_plugin/pyNN/control_models/live_packet_gather.py) which resides on **_chip 0,0_**. The [LivePacketGather](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007/spynnaker_external_devices_plugin/pyNN/control_models/live_packet_gather.py) then collates the packets and transmits them at the next available timer tic.

**NOTE:** Packets are relayed to a gathering point before being sent out down the Ethernet because letting the collection of cores transmit their packets directly to the Ethernet will result in multiple versions of the same header being transmitted. Because the Ethernet bandwidth is the biggest limiting factor on how much data can be transmitted, (**approximately 2820 bytes** per millisecond)  this means that reducing the number of headers is important. Gathering in a single point and sending one header saves bandwidth for the limitation of a 1 timer tic delay.

![Transmissions between cores](recievier_inside_spinnaker.jpg)

Each [Live_packet_gather](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007/spynnaker_external_devices_plugin/pyNN/control_models/live_packet_gather.py) is associated with a specific IP-Tag which controls what port and host is used when relaying packets outside a Ethernet port.

**NOTE:** Each Ethernet controlled chip has 8 iptags which are programmable, the tool chain automatically assigns these tags to each [live_packet_gather](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007/spynnaker_external_devices_plugin/pyNN/control_models/live_packet_gather.py) and so should not be worried about.

![IPTags](interface_between_chip_and_machine.png)

# <a name="constraints"></a> Constraints

The [reverse_iptag_multi_cast_vertex](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007/spynnaker_external_devices_plugin/pyNN/control_models/reverse_ip_tag_multi_cast_source.py) and the [live_packet_gather](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007/spynnaker_external_devices_plugin/pyNN/control_models/live_packet_gather.py) share these resources of the IP-Tags and the bandwidth of the Ethernet connection; therefore please use these models sparingly. 

The 2820 bytes per millisecond is a total bandwidth in both input and output through the Ethernet connection; therefore decisions must be made at compile time to what data should be transmitted. 

# <a name="liveoutput"></a> PyNN setting up for live output

This section defines how to set up a PyNN script to produce live_output by using the example[live_packet_output_synfire_chain](https://github.com/SpiNNakerManchester/PyNNExamples/tree/f742b9816e402558fe23bde31e8abcb266e709b5/examples/external_device_examples/receiving_scripts/live_packet_output_synfire_chain.py). The lines in the script requiring care are lines 7 and 64. Line 7 imports the ExternalDevicePlugin module and line 64 declares that the first population within this list is to be set for live output. 

`import spynnaker_external_devices_plugin.pyNN as q
`q.activate_live_output_for(populations[0])

# <a name="python_based"></a> Python Based Receiver

Creating a receiver from a python script, requires a "receiver" to be built which is set up to receive EIEIO Data packets. In a basic PyNN script, this could be build before **p.run()** is ran. 

NOTE: Recommendation is to create your listener in a separate file and run them in parallel. 

In [live_receiver](https://github.com/SpiNNakerManchester/PyNNExamples/tree/f742b9816e402558fe23bde31e8abcb266e709b5/examples/external_device_examples/receiving_scripts/live_receiver.py), a self contained script which registers a listener for a StrippedIPTagConnection and prints out the packet when received. 

The lines are as follows:

`from spinnman.connections.udp_packet_connections.stripped_iptag_connection \`
    `import StrippedIPTagConnection`
`from spinnman import constants`
`from spynnaker.pyNN.utilities.conf import config`
`import time`


`def packet_callback(packet):`
    `pass`
    `#Do something here`

`packet_grabber = \`
    `StrippedIPTagConnection(local_port=config.get("Recording", `
                                                  `"live_spike_port"))`
`packet_grabber.register_callback(packet_callback, `
                                 `constants.TRAFFIC_TYPE.EIEIO_DATA)`

`#sleep for the length of the simulation`

`time.sleep(XXXXXX)`

In the first 2 lines, can be seen the importing of a collection of classes from the Spinnman module. These are the connection which supports EIEIO data packets (these are what the [live_packet_gather](https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin/tree/2015.007/spynnaker_external_devices_plugin/pyNN/control_models/live_packet_gather.py) generates) and the constants used by the spinnman module. 

The next two imports are just to allow easier access to the end users spynnaker.cfg file and a function which will stop the thread from ending prematurely. 

The lines 8 and 9 defines a function which prints out a packet when called. 

Lines 11, 12 and 13 shows the definition of a connection which listens for EIEIO data packets on the default port used by the tool chain for packet output. 

Lines 14 and 15 register the function defined in lines 8 and 9 to be called when the connection receives a packet. 

Finally line 19 tells the thread to sleep, which will keep it running whilst the original PyNN script is set off, mapped and ran on the SpiNNaker machine. 

# <a name="c_based"></a> C Based Receiver

If interested in using a c based listener, refer to page [2.4 Visualiser framework](2015.003%3a-Just-Testing-%3a-2.4-Visualiser-framework)


# <a name="trouble"></a> Troubleshooting

**Packets are not coming out of SpiNNaker**

1. This could also be due to having a firewall configured to reject UDP packets. Configuring a firewall is os dependent, and so we do not focus on how to change the firewall here. 
