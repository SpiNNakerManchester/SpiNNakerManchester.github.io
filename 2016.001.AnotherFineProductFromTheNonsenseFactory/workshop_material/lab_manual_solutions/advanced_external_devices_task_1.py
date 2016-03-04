import pyNN.spiNNaker as p
import spynnaker_external_devices_plugin.pyNN as q
import pylab

p.setup(1.0)

injector = p.Population(
    10, q.SpikeInjector, {"virtual_key": 0x4200, "port": 18000},
    label="injector")
pop = p.Population(10, p.IF_curr_exp, {}, label="pop")
pop.record()

p.Projection(injector, pop, p.OneToOneConnector(weights=5.0))

p.run(7000)

spikes = pop.getSpikes()
spike_time = [i[1] for i in spikes]
spike_id = [i[0] for i in spikes]
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time (ms)")
pylab.ylabel("Neuron ID")
pylab.axis([0, 7000, -1, 10])
pylab.show()
