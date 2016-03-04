import pyNN.spiNNaker as p
import pylab
import numpy
from pyNN.random import RandomDistribution

p.setup(timestep=0.1)
n_neurons = 1000
n_exc = int(round(n_neurons * 0.8))
n_inh = int(round(n_neurons * 0.2))
weight_exc = 0.1
weight_inh = -5.0 * weight_exc

pop_exc = p.Population(n_exc, p.IF_curr_exp, {},
                       label="Excitatory")
pop_inh = p.Population(n_inh, p.IF_curr_exp, {},
                       label="Inhibitory")
stim_exc = p.Population(n_exc, p.SpikeSourcePoisson,
                        {"rate": 1000.0}, label="Stim_Exc")
stim_inh = p.Population(n_inh, p.SpikeSourcePoisson,
                        {"rate": 1000.0}, label="Stim_Inh")

delays_exc = RandomDistribution("normal", [1.5, 0.75], boundaries=(1.0, 14.4))
weights_exc = RandomDistribution("normal", [weight_exc, 0.1],
                                 boundaries=(0, numpy.inf))
conn_exc = p.FixedProbabilityConnector(0.1, weights=weights_exc,
                                       delays=delays_exc)
delays_inh = RandomDistribution("normal", [0.75, 0.375], boundaries=(1.0, 14.4))
weights_inh = RandomDistribution("normal", [weight_inh, 0.1],
                                 boundaries=(-numpy.inf, 0))
conn_inh = p.FixedProbabilityConnector(0.1, weights=weights_inh,
                                       delays=delays_inh)
p.Projection(pop_exc, pop_exc, conn_exc, target="excitatory")
p.Projection(pop_exc, pop_inh, conn_exc, target="excitatory")
p.Projection(pop_inh, pop_inh, conn_inh, target="inhibitory")
p.Projection(pop_inh, pop_exc, conn_inh, target="inhibitory")

conn_stim = p.OneToOneConnector(weights=weight_exc, delays=1.0)
p.Projection(stim_exc, pop_exc, conn_stim, target="excitatory")
p.Projection(stim_inh, pop_inh, conn_stim, target="excitatory")

pop_exc.initialize("v", RandomDistribution("uniform",
                                           [-65.0, -55.0]))
pop_inh.initialize("v", RandomDistribution("uniform",
                                           [-65.0, -55.0]))
pop_exc.record()
p.run(1000)

spikes = pop_exc.getSpikes()
pylab.plot([i[1] for i in spikes], [i[0] for i in spikes], "b.")
pylab.xlabel("Time (ms)")
pylab.ylabel("Neuron ID")
pylab.axis([0, 1000, -1, n_exc + 1])
pylab.show()
