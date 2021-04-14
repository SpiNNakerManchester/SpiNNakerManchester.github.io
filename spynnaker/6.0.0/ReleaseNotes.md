---
title: Release Notes for sPyNNaker version 6.0.0
layout: default
---

# Release notes for sPyNNaker v6.0

The software is now tested daily on python versions from 3.6 to 3.9.  We are now using GitHub Actions as well as our own local Jenkins server to perform such tests.

The following is a non-exhaustive list of the changes since v4.0 (some of which were available in v5.0 and v5.1 but have not been mentioned in release notes before):

## PyNN

 * Distance-dependent weights and delays are now permitted inside a synapse, dependent upon a specified function and space metric.
 * Projections are now allowed between PopulationViews, in the specific circumstance where the PopulationView is a contiguous region of a Population.
 * A lot of general tidying up and bug-fixing has been done as the code has matured and we have been presented with more and more use cases which occasionally find errors.

## PyNN-adjacent

### Structural Plasticity
 * It is now possible to specify a StructuralMechanismStatic or StructuralMechanismSTDP object as the synapse_type of a Projection, which allows the formation or elimination of synapses between the two Populations specified in the Projection based upon various rules.  See e.g. PyNN8Examples/examples/structural_plasticity_with_stdp_2d.py.

### SpikeSourcePoissonVariable
 * It is now possible to vary the rate of a SpikeSourcePoisson without having to have multiple calls to sim.run().  This is accessed via sim.extra_models.SpikeSourcePoissonVariable(...); for examples of use, see sPyNNaker/spynnaker_integration_tests/test_spike_source/test_variable_rate.py.

### Synchronized Execution
 * It is now possible to set up fixed periods of execution and then synchronize the runs in chunks of these periods with the host or some other external entity.  This is accessed by sim.external_devices.run_sync(run_time, sync_time) or sim.external_devices.run_forever(sync_time), where run_time is the total duration of the simulation, and sync_time is the chunk of time to run before pausing.  An external device must then send a sync signal for the simulation to continue; this can be sent using sim.external_devices.continue_simulation().

### KernelConnector
 * A new (SpiNNaker-specific) connector has been added which applies a (2D) kernel matrix of a specified shape to specify the connections between the pre- and post-populations on a Projection, which also require the definition of a (2D) shape matrix.  Optionally the user may also specify a weight and/or delay kernel matrix to allow for different weights to be specified, or simply define weights and delays in the synapse in the usual PyNN manner. See e.g. sPyNNaker/spynnaker_integration_tests/test_connectors/test_kernel_connector.py.

## SpiNNaker-specific updates

### Synaptic Expander
 * The synaptic matrices relating to a number of the PyNN connectors and the KernelConnector (see above) are now “expanded” using C code on the machine by default rather than on the host using Python, resulting in a large time-saving in building networks on the machine.

### Faster data I/O
 * The tools now use a new algorithm for loading and reading data which makes use of the multicast routers on the machine, and batched sending and receiving to increase the rate of the read and write operations.
 * A Java implementation of the algorithm can be optionally used, which allows thread-per-board loading and reading to take place (up to a specified number of threads), and so further reduce the time taken to load simulations and read back data.

### Population-based master population table
 * This allocates the master pop table on an app-vertex basis if possible. Note that this is detected using the keys; using the ZonedKeyAllocator (see below) will make this work in general, but the app keys are activated in other circumstances too.

### Mapping algorithms
 * A lot of improvements have been made to the underlying mapping algorithms on the machine, in particular relating to placement, compression and partitioning.
 * The ZonedKeyAllocator is now used by default; this attempts to assign keys to whole populations rather than just to cores, which can result in better compression, and can help with the Population-based master population table (see above).
 * The PairCompressor is now used by default; this uses a simple compression algorithm which works on pairs of routing entries, and leaves the most-used-route until last, and then uses a single entry to cover this route, reducing the amount of compression actually required.

### Spike filtering
 * This adds data to the local population table stored in DTCM on the SpiNNaker cores that stops the fetching of empty synaptic rows from SDRAM, reducing the time to process spikes that don’t target any neurons on certain cores.  This is done using an array of bits (or bitfield), which is only loaded on to the core if it fits into the local memory.
 * An additional algorithm is available which attempts to add entries to the local routing tables based on the bitfields above, and perform compression of these extended tables.  This means that spikes that don’t target neurons on the core will be filtered by the router avoiding the need to use the CPU to perform this filtering.  This algorithm can be very slow in execution however, so it is not enabled by default.

### Splitters
 * This is preparatory work to allow users more choice in how their network is placed onto the SpiNNaker machine; in particular with relation to PyNN, allowing the splitting of “neuron” and “synapse” cores and the creation of multiple “synapse” cores per “neuron” core.
 * As part of this work a lot of functionality has been moved from the ApplicationVertex into the MachineVertex.
 * Examples of Splitters that are in current use can be seen in PyNN8Examples/examples/partitioner_examples/splitter_usage.py

### Determinism
 * A lot of improvements have been made to the underlying code to make the code behave more deterministically (i.e. give the same answers each time identical user scripts are run).

### Documentation
 * Our documentation is now vastly improved for both C and Python code; this can generally be accessed for each repository via its main GitHub page / README file.

### Code size in ITCM
 * Various updates have been done to streamline the code size of binaries on the machine.




