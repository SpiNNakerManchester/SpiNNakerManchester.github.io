---
title: sPyNNaker Limitations
---

This guide will detail the limitations that sPyNNaker imposes on users of PyNN.


# PyNN version

sPyNNaker implements a subset of the [PyNN 0.7 API](http://neuralensemble.org/trac/PyNN/wiki/API-0.7).


# Model Type Limitations

sPyNNaker currently only supports the following model types:

1. IFCurrExp: Current based leaky integrate and fire, with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron
1. IFCondExp: Conductance based leaky integrate and fire, with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron
1. IFCurrDualExp: Current based, Leaky integrate and fire, with 2 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron
1. IZKCurrExp: Current based Izhikevich with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron 
1. IZKCondExp: Conductance based Izhikevich with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron 

Note that there are also further restrictions on what plasticity types are supported when used with the above models.


# External Input

sPyNNaker currently supports these two models for injecting spikes into a PyNN model:

1. SpikeSourceArray: Input of a pre-defined set of spikes.  The spikes to be input can be changed between calls to run.
1. SpikeSourcePoisson: Input of randomly generated spikes at a pre-defined mean rate generated from a Poisson distribution.

Currently, only the i_offset parameter of the neural models can be used to inject current directly; there is no support for noisy or step-based current input.


# Connectors

sPyNNaker currently supports the following connector types:

1. AllToAllConnector: All neurons in the pre-population are connected to all neurons in the post-population
1. DistanceDependentProbabilityConnector: The connectivity is random with a probability that depends on the distance between the neurons in the pre and post populations.
1. FixedNumberPreConnector: A fixed number of randomly selected neurons in the pre-population are connected to all neurons in the post-population.
1. FixedProbabilityConnector: The connectivity is random with a fixed probability of connection between any pair of neurons.
1. FromFileConnector: The connectivity is explicitly specified in a file, including all weights and delays.  Note that this connector will result in slower operation of the tools.
1. FromListConnector: The connectivity is explicitly specified in a list, including all weights and delays.  Note that this connector will result in slower operation of the tools. 
1. MultapseConnector: A fixed number of randomly selected connections are made.
1. OneToOneConnector: The neuron with index i in the pre-population is connected to the neuron with index i in the post-population.

# Plasticity

sPyNNaker currently only supports plasticity described by an ```STDPMechanism``` which is set as the ```slow``` property of ```SynapseDynamics```.

sPyNNaker supports the following STDP timing dependence rules:

1. PfisterSpikeTripletRule
1. SpikePairRule

and the following STDP weight dependence rules:

1. AdditiveWeightDependence
1. MultiplicativeWeightDependence

# sPyNNaker execution limitations

1. sPyNNaker supports the ability to call run() multiple times with different combinations of runtime values. 
1. sPyNNaker supports the ability to call reset() multiple times within the script with run() interleaved.
1. sPyNNaker supports the addition of vertices and edges into the application space between a reset() and a run(). 
1. sPyNNaker does not support the addition of vertices and edges between multiple calls to run().

# PyNN missing functionality

1. sPyNNaker does not support population views.
1. sPyNNaker does not support assemblers.
1. sPyNNaker does not support the changing of weights / delays / neuron parameters between the initial call to run() and a reset() call.


# Other Limitations
sPyNNaker also imposes the following limitations:

1. All of our neural models have a limitation of 255 neurons per core.  Depending on which SpiNNaker board you are using, this will limit the number of neurons that can be supported in any simulation.
1. All our models support delays between 1 timestep and 144 timesteps.  Delays of more than 16 timesteps are supported by delay extensions which take up another core within the machine, thus use of such delays will further limit the total number of neurons that can be supported in any simulation.
