---
title: sPyNNaker Limitations and Extensions
---

This guide will detail the limitations that sPyNNaker imposes on users of PyNN, as well as detailing some extensions to the PyNN language that are supported.


# PyNN version

sPyNNaker implements subsets of the [PyNN 0.7 API](http://neuralensemble.org/trac/PyNN/wiki/API-0.7) via the sPyNNaker7 module, or the [PyNN 0.8 API](http://neuralensemble.org/docs/PyNN/0.8/api_reference.html) via the sPyNNaker8 module.


# Neuron Model Limitations

sPyNNaker currently supports the following model types:

1. IFCurrExp: Current-based leaky integrate and fire, with 1 excitatory and 1 inhibitory exponentially-decaying synaptic input per neuron
1. IFCondExp: Conductance-based leaky integrate and fire, with 1 excitatory and 1 inhibitory exponentially-decaying synaptic input per neuron
1. IFCurrDualExp: Current-based leaky integrate and fire, with 2 excitatory and 1 inhibitory exponentially-decaying synaptic input per neuron
1. IZKCurrExp: Current-based Izhikevich with 1 excitatory and 1 inhibitory exponentially-decaying synaptic input per neuron (Note: in sPyNNaker8, this model is called "Izhikevich")
1. IZKCondExp: Conductance-based Izhikevich with 1 excitatory and 1 inhibitory exponentially-decaying synaptic input per neuron (Note: in sPyNNaker8, this model is called "Izhikevich_cond")
1. IFCurrDelta: Current-based leaky integrate and fire, with instantaneous current input per neuron
1. IFCurrExpCa2Adaptive: Current-based spike-frequency adaptation of a generalised leaky integrate and fire neuron
1. IfCondExpStoc: Conductance-based leaky intergate and fire with a stochastic Maass threshold.

Note that there are also further restrictions on what plasticity types are supported when used with the above models.

All of our neural models have a limitation of 255 neurons per core.  Depending on which SpiNNaker board you are using, this will limit the number of neurons that can be supported in any simulation.


# External Input

sPyNNaker currently supports these two models for injecting spikes into a PyNN model:

1. SpikeSourceArray: Input of a pre-defined set of spikes.  The spikes to be input can be changed between calls to run.
1. SpikeSourcePoisson: Input of randomly generated spikes at a pre-defined mean rate generated from a Poisson distribution.

Currently, only the i_offset parameter of the neural models can be used to inject current directly; there is no support for noisy or step-based current input.

A third, none standard PyNN interface, way of injecting current into a PyNN simulation executing on the hardware is through live injection from an external device. These functions are supported by our sPyNNakerExternalDevicesPlugin.  A description on how to use this functionality can be found [here](SimpleIO-LabManual.pdf).


# Connectors

sPyNNaker currently supports the following connector types:

1. AllToAllConnector: All neurons in the pre-population are connected to all neurons in the post-population
1. DistanceDependentProbabilityConnector: The connectivity is random with a probability that depends on the distance between the neurons in the pre and post populations.
1. FixedNumberPreConnector: A fixed number of randomly selected neurons in the pre-population are connected to all neurons in the post-population.
1. FixedNumberPostConnector: A fixed number of randomly selected neurons in the post-population are connected to all neurons in the pre-population.
1. FixedProbabilityConnector: The connectivity is random with a fixed probability of connection between any pair of neurons.
1. FromFileConnector: The connectivity is explicitly specified in a file, including all weights and delays.  Note that this connector will result in slower operation of the tools.
1. FromListConnector: The connectivity is explicitly specified in a list, including all weights and delays.  Note that this connector will result in slower operation of the tools.
1. MultapseConnector: A fixed number of randomly selected connections are made.
1. OneToOneConnector: The neuron with index i in the pre-population is connected to the neuron with index i in the post-population.
1. SmallWorldConnector: Connect cells so as to create a small-world network.

# Plasticity

sPyNNaker currently only supports plasticity described by an ```STDPMechanism``` which is set as the ```slow``` property of ```SynapseDynamics```.

sPyNNaker supports the following STDP timing dependence rules:

1. PfisterSpikeTriplet
1. SpikePairRule
1. Vogels2011Rule
1. RecurrentRule
1. SpikeNearestPair

and the following STDP weight dependence rules:

1. AdditiveWeightDependence
1. MultiplicativeWeightDependence
1. WeightDependenceAdditiveTriplet

# sPyNNaker execution limitations

1. sPyNNaker supports the ability to call run() multiple times with different combinations of runtime values.
1. sPyNNaker supports the ability to call reset() multiple times within the script with run() interleaved.
1. sPyNNaker supports the addition of vertices and edges into the application space between a reset() and a run().
1. sPyNNaker does not support the addition of vertices and edges between multiple calls to run().

# PyNN missing functionality

1. sPyNNaker does not support population views.
1. sPyNNaker does not support assemblers.
1. sPyNNaker does not support the changing of weights / delays / neuron parameters between the initial call to run() and a reset() call.

# Parameter ranges

All parameters and their ranges are under software control.

Weights are held as 16-bit integers, with their range determined at compile-time to suit the application; this limits the overall range of weights that can be represented, with the smallest representable weight being dependent on the largest weights specified.

There is a limit on then length of delays of between 1 and 144 time steps (i.e. 1 - 144ms when using 1ms time steps, or 0.1 - 14.4ms when using 0.1ms time steps).  Delays of more than 16 time steps require an additional "delay population" to be added; this is done automatically by the software when such delays are detected.

Membrane voltages and other neuron parameters are generally held as 32-bit fixed point numbers in the s16.15 format.  Membrane voltages are held in mV.

# Synapse and neuron loss

Projection links between two sub-populations that were initially defined as connected are removed by the software if the number of connections between the two sub-populations is determined to be zero when the projection is realised in
the software's mapping process.

The SpiNNaker communication fabric can drop packets, so there is the chance that, during execution, spikes might not reach their destination (or might only reach some of their destinations).  The software attempts to recover from such losses through a reinjection mechanism, but this will only work if the overall spike rate is not high enough to overload the communications fabric in the first place.
