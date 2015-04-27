---
title: AER_dev_sim: An external device simulator for EIEIO interfacing
---

# Introduction

AER_dev_sim is a C++ host-based device simulator that can emulate an external device communicating with SpiNNaker via the EIEIO interface. This can be used in 3 different scenarios: as a debug tool to examine protocol and communications from the SpiNNaker board; as a software tester for a proposed interface for an external device; as a virtual device for a running simulation, that can either source or sink spikes on the
SpiNNaker platform. It supports a wide variety of options including ones to set up the basic communication parameters, ones to specify various spike handling modes, ones that set address-mapping parameters, and ones that set the run-time behaviour of the virtual device. To invoke AER_dev_sim you type the command plus options, hence:

    ./AER_dev_sim -a 130.88.196.21 -p 12345 -s 1 -h

or similar. The following sections explain the various available options. Each **option** gives the option letter, followed by what type of [value] is expected, followed by its default value, if any, _in italics_ and then the description. Thus:

**-Z** [hex code] _0_
### Not a real option - crash with a code
This option causes the simulator to crash and exit with a code specified by the hex value.

# Option Descriptions

***

## Basic Communication Parameters

**-a** [hex or octet form (xx.xx.xx.xx) ip address] _127.0.0.1_
### SpiNNaker IP address
This sets the IP address of the SpiNNaker board with which you wish to communicate

**-p** [decimal port number] _16384_
### Communication port
This sets the UDP port that the device expects to communicate using.

**-g** [decimal tag] _0_
### AER Tag
This sets a tag in the Tag field of the AER packet, according to the specification.

**-y** [decimal default payload] _0_
### Packets have payloads
This sets the virtual device to expect payloads in received packets and generate them in sent packets. The default payload will be used when sending packets unless other options provide additional payload data.

**-n** [decimal number] _1_
### Number of spikes per sent packet
This sets the number of spikes that will be sent in each issued packet. The valid range is 0-256. The virtual device will attempt to collect this many spikes before sending, unless a timeout is set.

**-h**
### Halfword key/payload size
By default, the interface expects/issues 32-bit keys and payloads. Setting this switch will cause it to issue 16-bit keys and payloads and truncate any 32-bit keys/payloads received to 16-bit.

**-v** 
### Payloads are timestamps
This is a value-less switch that sets the interface to expect that received payloads are timestamps and to generate timestamps (according to the local system time) when packets are sent.

***

## Spike Generation Modes

**-s** [decimal mode] _0_
### Spike Source Mode
This controls how the virtual device will source spikes, if at all. Valid options are in the range 0-3. 0 means receive only, do not issue spikes, 1 means reflect any received spikes back as issued spikes, 2 means actively source spikes, either generated automatically or read from a file, and 3 means actively source spikes AND reflect received spikes.

**-c** [decimal or hex command]
### Command Packet
This sets the virtual device to issue a command packet as specified by the code. The user _must_ specify the command when using this option. It is not advised to set the interface to pack more spikes into a packet than 1 when using this option. Repeats could be specified but could result in unexpected behaviour on the SpiNNaker side. The interface can always _receive_ commands but will do nothing special with them, i.e. a device-specific command issued from SpiNNaker will not cause any configuration or state change in the virtual device.

**-e** [decimal value] _0_
### Payload prefix
This sets the virtual device to issue packets with a payload prefix as specified. The payload-prefixed packet type will be used.

**-r** [decimal repeat count] _1_
### Number of spikes to repeat
For issued spikes, this sets a number of repeats, for each spike generated or read from a file. The interface will generate _repeat_count_ duplicates of the spike, possibly splitting them across multiple packets. If an increment is set each repeated spike will increment by the specified amount.

**-f** [text filename]
### Input file for issued spikes 
This instructs the virtual device to generate spikes from the specified file. It will process each spike in the order it appears in the file.

**-o** [text file name]
### Output file for received spikes
This instructs the virtual device to dump received spikes (after masking and key processing) to a file.

***

## Address-mapping parameters

**-d** [decimal or hex prefix] _0_
### Spike absolute prefix
This sets the virtual device to OR an absolute prefix to each spike sent. The operation occurs prior to any key prefixing in the packet itself. Thus, all spikes in the packet will have this prefix in their literal key sent or received. With this option the user can set ANY prefix in the range 0-4294967295 (0x0-0xFFFFFFFF).

**-k** [decimal or hex prefix value] _0_
### Key prefix
This will cause issued spikes to be sent with a key prefix equal to the value set. Prefixes should be in the range 0-65535 (0x0-0xFFFF). Outgoing packets will be set to be of prefixed type.

**-b** [decimal or hex mask] _0_
### Spike key bitmask
This applies a mask, immediately before sending, and as the last step in receiving, to any keys. Only those parts of the key which have a binary 1 in the bit will survive and be sent or received. Thus, the user can map out irrelevant parts of the key over the interface.

**-m** [decimal ID] _0_
### Minimum spike ID
This sets the lowest spike ID the virtual device will send. Spike ID's lower than this will be clipped at the minimum value. The interface will also clip received spikes to fall within the range. The value is considered before any prefixing or masking operations are performed.

**-x** [decimal ID] _2047_
### Maximum Spike ID
This sets the highest spike ID the virtual device will send. Spike ID's higher than this will be clipped at the maximum value. The interface will also clip received spikes to fall within the range. The value is considered before any prefixing or masking operations are performed.

**-i** [decimal increment] _0_
### Spike ID increment
With repeating spikes, the virtual device can be set to auto-increment the ID, sweeping a range of values. This option sets the size of the increment. If an increment causes the spike to fall outside the [min, max] range the ID will be clipped as usual.

**-u**
### Key prefix in upper halfword
With this switch set, and if a prefixed key type is indicated for issued spikes, the virtual device will indicate that the prefix should be in the upper halfword. Otherwise it will prefix the lower halfword. 
 
**-w**
### Wrap spike IDs
If this switch is set, the virtual device, rather than clipping to any maximum or minimum value, will wrap the ID using modulo-[max-min] to set the actual spike ID.


***

## Run-time Behaviour

**-t** [decimal timeout] _0_
### Timeout in ms
This option sets a timeout for issuing spikes. If, when the timeout expires, _num_spikes_per_packet_ spikes (according to the -n option) have not been received or read, the virtual device will immediately send any spikes already received or read.

**-l**
### Continuous looping mode
For virtual devices that generate auto-incrementing spikes or that read from a file, the program will automatically end when the increment reaches the top or the file is exhausted. In continuous looping mode, the program will continue, looping to the beginning of any file (and truncating auto-incremented spikes unless the wrap option has been set) and continuing. (This option has no effect on virtual devices set to receive only, which stay active until CTRL+C is pressed.)
