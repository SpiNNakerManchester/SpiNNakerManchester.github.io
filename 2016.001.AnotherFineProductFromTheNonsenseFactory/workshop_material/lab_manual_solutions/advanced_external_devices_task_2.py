import pyNN.spiNNaker as p
import spynnaker_external_devices_plugin.pyNN as q
from spinnman.messages.eieio.eieio_type import EIEIOType

p.setup(1.0)

#pop = p.Population(4, p.SpikeSourceArray, {"spike_times": [[0], [1000], [2000], [3000]]})
pop = p.Population(4, p.SpikeSourcePoisson, {"rate": 5})
q.activate_live_output_for(
    pop, port=18000, message_type=EIEIOType.KEY_16_BIT,
    payload_as_time_stamps=False, use_payload_prefix=False)

p.run(5000)
