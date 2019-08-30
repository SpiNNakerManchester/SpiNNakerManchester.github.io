---
title: sPyNNaker Models, Limitations and Extensions
---

This guide will detail the limitations that sPyNNaker imposes on users of PyNN, as well as detailing some extensions to the PyNN language that are supported.


# PyNN version

sPyNNaker8 implements a subset of the [PyNN 0.9 API](http://neuralensemble.org/docs/PyNN/0.9/api_reference.html).

**We _recommend_ using PyNN 0.9 for new work.**

# Neuron Models

sPyNNaker currently supports the following model types:

1. `IF_curr_exp`: Current based leaky integrate and fire, with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron
1. `IF_cond_exp`: Conductance based leaky integrate and fire, with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron
1. `IF_curr_alpha`: Current based leaky integrate and fire, with 1 excitatory and 1 inhibitory alpha-function shaped synaptic input per neuron
1. `extra_models.IF_curr_dual_exp`: Current based, Leaky integrate and fire, with 2 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron
1. `Izhikevich`: Current based Izhikevich with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron
1. `extra_models.Izhikevich_cond` (PyNN 0.8): Conductance based Izhikevich with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron
1. `extra_models.IFCurDelta`: Current based leaky integrate and fire with 1 excitatory and 1 inhibitory delta synaptic input per neuron
1. `extra_models.IFCurrExpCa2Adaptive`: Current based leaky integrate and fire with 1 excitatory and 1 inhibitory exponentially decaying, calcium-adaptive synaptic input per neuron
1. `extra_models.IFCondExpStoc`: Conductance-based leaky intergate and fire with a stochastic Maass threshold.
1. `extra_models.IF_curr_exp_sEMD`: Current based leaky integrate and fire with 1 excitatory and 1 inhibitory exponentially decaying synaptic input per neuron where the inhibitory input is scaled by a multiplicative factor defined by the user

Note that there are further restrictions on what plasticity types are supported when used with the above models.

All of our neural models have a limitation of 255 neurons per core.  Depending on which SpiNNaker board you are using, this will limit the number of neurons that can be supported in any simulation.

# External Input

sPyNNaker currently supports two models for injecting spikes into a PyNN model:

1. `SpikeSourceArray`: Input of a predefined set of spikes.  The spikes to be input can be changed between calls to run.
1. `SpikeSourcePoisson`: Input of randomly generated spikes at a predefined mean rate generated from a Poisson distribution.

Currently, only the `i_offset` parameter of the neural models can be used to inject current directly; there is no support for noisy or step-based current input.  Step-based current input can be achieved by updating `i_offset` between calls to `run()`.

A third, non-standard PyNN interface, way of injecting current into a PyNN simulation executing on the hardware is through live injection from an external device (e.g., a robot). A description on how to use this functionality can be found [here](SimpleIO-LabManual.pdf).

# Connectors

sPyNNaker currently supports the following connector types:

1. `AllToAllConnector`: All neurons in the pre-population are connected to all neurons in the post-population
1. `ArrayConnector`: The connectivity is set by passing in an explicit boolean array matrix of size (pre-population size, post-population size).
1. `CSAConnector`: The connectivity is set due to a Connection Set Algebra as defined by [Djurfeldt (2012)](https://www.ncbi.nlm.nih.gov/pubmed/22437992).  For more information on the python implementation see [github.com/INCF/csa](https://github.com/INCF/csa).
1. `DistanceDependentProbabilityConnector`: The connectivity is defined by a probability that depends on the distance between the neurons in the pre- and post-populations.
1. `FixedNumberPreConnector`: A fixed number of randomly selected neurons in the pre-population are connected to all neurons in the post-population.
1. `FixedNumberPostConnector`: A fixed number of randomly selected neurons in the post-population are connected to all neurons in the pre-population.
1. `FixedProbabilityConnector`: The connectivity is random with a fixed probability of connection between any pair of neurons.
1. `FromFileConnector`: The connectivity is explicitly specified in a file, including all weights and delays.  Note that this connector will result in slower operation of the tools.
1. `FromListConnector`: The connectivity is explicitly specified in a list, including all weights and delays.  Note that this connector will result in slower operation of the tools.
1. `FixedTotalNumberConnector`: A fixed number of randomly selected connections are made.
1. `IndedxDependentProbabilityConnector`: The connectivity is defined by a probability that depends on the indices of the neurons in the pre- and post-populations.
1. `KernelConnector`: The pre- and post-populations are considered as a 2D array, and every post(row, col) neuron connects to many pre(row, col, kernel) using a (kernel) set of weights and/or delays.
1. `OneToOneConnector`: The neuron with index _i_ in the pre-population is connected to the neuron with index _i_ in the post-population.
1. `SmallWorldConnector`: Connect cells so as to create a small-world network.

# Plasticity

sPyNNaker8 currently only supports plasticity described by an `STDPMechanism` which is set as the `synapse_dynamics` property of a `Projection`.

sPyNNaker supports the following STDP timing dependence rules:

1. `SpikePairRule`: The amount of potentiation or depression decays exponentially with the time between each pair of pre and post spikes.
1. `extra_models.SpikeNearestPair`: Similar to the SpikePairRule, but only the nearest pair of pre and post spikes are considered i.e. the pre-spike that immediately follows a post spike or the post spike that immediately follows a pre-spike
1. `extra_models.PfisterSpikeTripletRule`:
1. `extra_models.Vogels2011Rule`:
1. `extra_models.RecurrentRule`:

and the following STDP weight dependence rules:

1. `AdditiveWeightDependence`: The change in weight is related only to the timing between the spikes determined by the timing rule.
1. `MultiplicativeWeightDependence`: The change in weight is related additionally to difference between the current and the maximum / minimum allowed weight of the rule.
1. `extra_models.WeightDependenceAdditiveTriplet`: As with AdditiveWeightDependence but allows the use of triplet rules.

# Limitations

## sPyNNaker execution limitations

1. sPyNNaker supports the ability to call `run()` multiple times with different combinations of runtime values.
1. sPyNNaker supports the ability to call `reset()` multiple times within the script with `run()` interleaved.
1. sPyNNaker supports the addition of Populations and Projections into the application space between a `reset()` and a `run()`.
1. sPyNNaker does not support the addition of Populations and Projections between multiple calls to `run()`, i.e., `reset()` must be called before a Population or Projection is added.

## PyNN missing functionality

1. sPyNNaker does not support `PopulationView` or accessing individual neurons in a `Population`.
1. sPyNNaker does not support `Assembly`.
1. sPyNNaker does not support the changing of weights or delays between calls to `run()`, i.e., `reset()` must be called before changes to weights and delays are made.

## Parameter ranges

All parameters and their ranges are under software control.

Weights are held as 16-bit integers, with their range determined at compile-time to suit the application; this limits the overall range of weights that can be represented, with the smallest representable weight being dependent on the largest weights specified.

There is a limit on the length of delays of between 1 and 144 time steps (i.e., 1 - 144ms when using 1ms time steps, or 0.1 - 14.4ms when using 0.1ms time steps).  Delays of more than 16 time steps require an additional "delay population" to be added; this is done automatically by the software when such delays are detected.

Membrane voltages and other neuron parameters are generally held as 32-bit fixed point numbers in the s16.15 format.  Membrane voltages are held in mV.

## Synapse and neuron loss

Projection links between two sub-populations that were initially defined as connected are removed by the software the number if the number of connections between the two sub-populations is determined to be zero when the projection is realised in
the software's mapping process.

The SpiNNaker communication fabric can drop packets, so there is the chance that during execution that spikes might not reach their destination (or might only reach some of their destinations).  The software attempts to recover from such losses through a reinjection mechanism, but this will only work if the overall spike rate is not high enough to overload the communications fabric in the first place.
