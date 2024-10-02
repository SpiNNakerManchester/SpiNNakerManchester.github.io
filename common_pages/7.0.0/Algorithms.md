---
title: Controlling which algorithms are run in the SpiNNaker tool-chain
published: true
---

This page describes changes made since the 6.0.0 release.

# Contents
* [Configuration Files](#Files)
* [Mode](#Mode)
* [Reports](#Reports)
* [Mapping Stardard Usage](#Standard)
* [Running alternative algorithms](#Alternative)
* [Running your own algorithms](#Own)

# <a name="Configuration Files"></a> Configuration Files
The system will read configuration files from various places.
The rule is last in only out, so if a later file provides a different configuration value that will overwrite any previous one.
Every run reports the list of config files read in the order they were read.

## Files included on the code base
The files include in the code base such as spinn_front_end_common/interface/spinnaker.cfg, spynnaker/pyNN/spynnaker.cfg and 
spinnaker_graph_front_end/spiNNakerGraphFrontEnd.cfg contain system defaults.

Do not edit the cfg files in the codebase.

## File in your home directory.
The .spynnaker.cfg (for PyNN) or .spiNNakerGraphFrontEnd.cfg (for GraphFrontEnd) contains your personal settings for running all scripts.

This includes how you connect to the system.
See [Configuration](spynnaker/PyNNOnSpinnakerInstall.html#Configurationl)

It can also hold you personal preferences for Reports, Mode and Mapping

### File local to the script
The final place the system will check for a configuration file is in the directory from which you run your script.

The optional spynnaker.cfg (for PyNN) or spiNNakerGraphFrontEnd.cfg (for GraphFrontEnd) holds the values you want to apply only to the script in this folder.

# <a name="Mode"></a> Mode
The cfg setting \[Mode\] mode is used to quickly turn on all reports.

The value Production will run just those reports requested

The value Debug will turn on all reports.  
It will also list the cfg settings changed so you can pick the ones that match the reports you are interested in.

For versions 7.3.0 or later see [cfg_file](common_pages/cfg_file.md#mode)

# <a name="Reports"></a> Reports

This section contains the flags for turning on or off specific reports.

The best way to see which reports are currently available, and the cfg flags is to run a small script with mode = Debug

The flag reports_enabled = False will turn off all reports and list the cfg setting that have been changed.

## where reports are written to
The setting default_report_file_path controls where the reports are written.

We recommend setting a file path as otherwise reports will build up in all directories you run scripts from.

# <a name="Standard"></a> Mapping standard Usage for most users

The tool chain comes preconfigured to run the algorithms which are most likely 
to work well for most users in most use cases.
Therefor unless you have a known reason to use a none default agorithm we suggest you remove the whole \[Mapping]\ section from your home and local configurations file(s).

The default algorithms are the ones we run most of our tests with.

# <a name="Alternative"></a> Running alternative algorithms
Most users will not need to use alternative algorithm.

To use an alternative just use the algorithm type = name. For example:

placer = OneToOnePlacer

This section does not include all the currently available alternative algorithms, listing only the ones we see a reason to support longer term.

Most of the none listed algorithms are kept mainly for historical and comparative reasons but could be removed at any time.

If you use another alternative algorithm not listed here please let us know so we know to continue to support it longer term. 

## Previous values
The cfg values used up to version 6.0 are no longer supported and will raise an exception.

These are loading_algorithms, application_to_machine_graph_algorithms,  machine_graph_to_machine_algorithms and
machine_graph_to_virtual_machine_algorithms

Unless there is a known specific reason for running a none default algorithm you can safely just delete these cfg settings.

## placer
This controls on which board/ chip core each vertex is placed.

#### RadialPlacer
This is the simplest of the placers which allocates the chip as close as possible to the starting point,
typically 0, 0

All the other placers extend this one

#### OneToOnePlacer
This placer looks for vertices pairs of vertices where the first only sends to the second and the second only receives from the first.
As far as possible these are then placed on the same Chip.

#### SpreaderPlacer
This placer attempts to distribute the vertices over as many Chips as possible.

The affect is most noticable if the script requests more boards than it actaully neeeds.

The current version does not scale well on very large jobs so we recommend using the RadialPlacer for very large jobs

## info_allocator
This controls which keys are assigned to which vertices.

#### ZonedRoutingInfoAllocator
This tries to allocate keys by Application vertex/ Population and in such a way that the compressor has the best chance of success.

## router
This determins how the spikes and other messages are sent between vertices.
Ie over which Chips the message passes.

#### NerRouteTrafficAware
This is a nearest neighbour router that takes what it knows about the trafic into consideration.

## compressor
This determins how the routing information is compressed to fit in the maximum of 1024 allowed entries.

They are distinquished in various ways.

1. On host vs on chip.  We always recommend using an on Chip version as these run in parallel.
The on host ones are manly kept for testing and ease of understanding
   
2. Pair vs OrderedCovering
OrderedCovering is the original compresssion algorithm developed by Mundy which leave the default routes (ones that keep going in the same direction)
as the ones that do not need including in the compressed table. All other routes are compressed grouped by destination with any hard cases handled first.
   
Pair is the current algorithm which so far has shown better results in nearly all cases.
The Pair compressor works through all the routes trying to merge pairs of routes rather than whole blocks. 
It also sorts the entries by destination, removing all the ones that go to the most popular destination.
   
3. BitFields
The bitfield compressors create a routing entry for every single neuron in the vertex and then remove ones that never receive from that source.
They have been shown to reduce the number of spikes/message that have to be dealt with.
However as they can get slow for large networks they are currently not used.
   
4. Spynnaker
For some compressors a specific PyNN version exists which makes use of things only found when using PyNN

#### PairOnChipRouterCompression

An on chip compressor that uses the pair method, but does not take bitfields into consideration.
The same algorithms work for PyNN and well as none PyNN scipts

#### OrderedCoveringOnChipRouterCompression

An on chip compressor that uses the OrderedCovering method, but does not take bitfields into consideration.
The same algorithms work for PyNN and well as none PyNN scripts

Previously known by various names including the word Mundy

#### SpynnakerMachineBitFieldPairRouterCompressor

An on chip compressor that uses the Pair methods and takes bitfields into consideration.
The same algorithms work for PyNN scripts

## virtual_compressor
A seperate setting to allow you to switch compressors if using a virtual board

Leave as None will cause the system to use and probably skip the one set by compressor

Only needed if testing compressors or later algorithms that need a compressed routing tree

## delay_support_adder
This setting is only used for PyNN Scripts

#### DelaySupportAdder

Adds delay supoort vertices where required.

#### None

Disables the adding of delay support vertices.  
Note if the receiving vertex/ Population can not handle the requested delay this will cause an exception.

# <a name="Own"></a> Running your own algorithms

The way to add your own algorithms has completely changed since version 6.0.

The xml description files are no longer used.

Adding your own algorithms is relatively easy but now does require a minor change to the code base.
This applies to both the algorithms which already have a cfg flag as well as any that don't.

This is specifically undocumented as we would like to hear what algorithms are being added and why.
An algorithm (including reports) that is useful to one user many be interesting to other so could be worth adding to the general code base.



