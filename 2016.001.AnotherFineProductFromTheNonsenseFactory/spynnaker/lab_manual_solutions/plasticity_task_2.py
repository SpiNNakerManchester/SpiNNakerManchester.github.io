#!/bin/python

import pyNN.spiNNaker as p

p.setup(timestep=1.0, min_delay=1.0, max_delay=16.0)

cell_params_lif = {'cm'        : 0.25, # nF
                   'i_offset'  : 0.0,
                   'tau_m'     : 20.0,
                   'tau_refrac': 2.0,
                   'tau_syn_E' : 5.0,
                   'tau_syn_I' : 5.0,
                   'v_reset'   : -70.0,
                   'v_rest'    : -65.0,
                   'v_thresh'  : -50.0
                   }

weight_to_spike = 2.0

ssa1_times = {'spike_times': [[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190]]}
ssa2_times = {'spike_times': [[8, 18, 28, 38, 48, 58, 68, 78, 88, 98]]}

lif1 = p.Population(1, p.IF_curr_exp, cell_params_lif, label='lif1')
lif2 = p.Population(1, p.IF_curr_exp, cell_params_lif, label='lif2')

ssa1 = p.Population(1, p.SpikeSourceArray, ssa1_times, label='ssa1')
ssa2 = p.Population(1, p.SpikeSourceArray, ssa2_times, label='ssa2')

t_rule = p.SpikePairRule (tau_plus=5, tau_minus=5)
w_rule = p.AdditiveWeightDependence (w_min=0.0, w_max=weight_to_spike, A_plus=weight_to_spike, A_minus=weight_to_spike)
stdp_model = p.STDPMechanism (timing_dependence = t_rule, weight_dependence = w_rule)
s_d = p.SynapseDynamics(slow = stdp_model)

input_proj = p.Projection(lif1, lif2, p.AllToAllConnector(weights=(weight_to_spike / 2.0), delays=1), synapse_dynamics = s_d, target="excitatory")
start_proj = p.Projection(ssa1, lif1, p.AllToAllConnector(weights=weight_to_spike, delays=1), target="excitatory")
teaching_proj = p.Projection(ssa2, lif2, p.AllToAllConnector(weights=weight_to_spike, delays=1), target="excitatory")

lif1.record()
lif2.record()

p.run(200)

spikes1 = lif1.getSpikes()
spikes2 = lif2.getSpikes()
weights = input_proj.getWeights()

print "Spikes generated by lif1: ", spikes1
print "Spikes generated by lif2: ", spikes2
print "final synaptic weight: ", weights