import pyNN.spiNNaker as p
import pylab

p.setup(1.0)

input = p.Population(
    1, p.SpikeSourceArray, {"spike_times": [0.0]}, label="input")

synfire_pop = p.Population(100, p.IF_curr_exp, {}, label="synfire")

p.Projection(input, synfire_pop, p.FromListConnector([(0, 0, 5.0, 1.0)]))

synfire_list = []
for n in range(0, 100):
    synfire_list.append((n, (n + 1) % 100, 5.0, 5.0))
p.Projection(synfire_pop, synfire_pop, p.FromListConnector(synfire_list))

synfire_pop.record()
p.run(2000)

spikes = synfire_pop.getSpikes()
spike_time = [i[1] for i in spikes]
spike_id = [i[0] for i in spikes]
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time (ms)")
pylab.ylabel("Neuron ID")
pylab.axis([0, 2000, 0, 100])
pylab.show()
