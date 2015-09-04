import pyNN.spiNNaker as p
import pylab

p.setup(1.0)

input = p.Population(2, p.SpikeSourceArray, {"spike_times": [[0.0], [1.0]]},
                     label="input")
pop = p.Population(2, p.IF_curr_exp, {"tau_syn_E": 1.0}, label="pop")
pop.record()
pop.record_v()

p.Projection(input, pop, p.OneToOneConnector(weights=5.0, delays=2.0))

p.run(10)

spikes = pop.getSpikes()
spike_time = [i[1] for i in spikes]
spike_id = [i[0] for i in spikes]
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time (ms)")
pylab.ylabel("Neuron ID")
pylab.axis([0, 10, -1, 2])
pylab.show()

print pop.get_v()
