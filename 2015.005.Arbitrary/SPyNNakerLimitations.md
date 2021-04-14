---
title: sPyNNaker Limitations
---
# The version described here is no longer supported. 

[Home page for current version](/) 

This guide will detail the limitations that sPyNNaker imposes on users of PyNN.


# PyNN version

sPyNNaker implements a subset of the [PyNN 0.7 API](http://neuralensemble.org/trac/PyNN/wiki/API-0.7).


# Model Type Limitations

sPyNNaker currently only supports the following model types:

1. Leaky intergrate and fire current exponential [IFCurrExp](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_models/if_curr_exp.py)
1. Leaky intergrate and fire conductive exponential [IFCondExp](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_models/if_cond_exp.py) 
1. Leaky intergrate and fire duel current exponential [IFCurrDualExp](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_models/if_curr_dual_exp.py)
1. Izhikevich Current Exponential Population [IZKCurrExp](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_models/izk_curr_exp.py)


# External Input

sPyNNaker currently supports these two models for injecting spikes into a PyNN model:

1. Spike source array [SpikeSourceArray](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/spike_source/spike_source_array.py)
1. Spike source poisson [SpikeSourcePoisson](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/spike_source/spike_source_poisson.py)

Currently, only the i_offset parameter of the neural models can be used to inject current.


# Connectors

sPyNNaker currently supports the following connector types:

1. All to All connector [AllToAllConnector](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_projections/connectors/all_to_all_connector.py)
1. Distance dependent probability connector [DistanceDependentProbabilityConnector](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_projections/connectors/distance_dependent_probability_connector.py)
1. Fixed number pre connector [FixedNumberPreConnector](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_projections/connectors/fixed_number_pre_connector.py)
1. Fixed probability connector [FixedProbabilityConnector](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_projections/connectors/fixed_probability_connector.py)
1. From file connector [FromFileConnector](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_projections/connectors/from_file_connector.py)
1. From list connector [FromListConnector](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_projections/connectors/from_list_connector.py)
1. Multapse connector [MultapseConnector](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_projections/connectors/multapse_connector.py)
1. One to one connector [OneToOneConnector](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_projections/connectors/one_to_one_connector.py)

# Plasticity

sPyNNaker currently only supports plasticity described by an ```STDPMechanism``` which is set as the ```slow``` property of ```SynapseDynamics```.

sPyNNaker supports the following STDP timing dependence rules:

1. Pfister spike triplet rule [PfisterSpikeTripletRule](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_properties/synapse_dynamics/dependences/pfister_spike_triplet_time_dependence.py)
1. Spike pair rule [SpikePairRule](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_properties/synapse_dynamics/dependences/spike_pair_time_dependency.py)

and the following STDP weight dependence rules:

1. Additive weight dependence [AdditiveWeightDependence](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_properties/synapse_dynamics/dependences/additive_weight_dependence.py)
1. Multiplicative weight dependence [MultiplicativeWeightDependence](https://github.com/SpiNNakerManchester/sPyNNaker/tree/2015.005/spynnaker/pyNN/models/neural_properties/synapse_dynamics/dependences/multiplicative_weight_dependence.py)


# Other Limitations
sPyNNaker also imposes the following limitations:

1. All of our neural models have a limitation of 256 neurons per core.  Depending on which SpiNNaker board you are using, this will limit the number of neurons that can be supported in any simulation.
1. All our models support delays between 1 timestep and 144 timesteps.  Delays of more than 16 timesteps are supported by delay extensions which take up another core within the machine, thus use of such delays will further limit the total number of neurons that can be supported in any simulation.
