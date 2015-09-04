# imports of both spynnaker and external device plugin.
import spynnaker.pyNN as Frontend
import spynnaker_external_devices_plugin.pyNN as ExternalDevices
from spynnaker_external_devices_plugin.pyNN.connections\
    .spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection
# plotter in python
import pylab
from threading import Condition
# initial call to set up the front end (pynn requirement)
Frontend.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
# neurons per population and the length of runtime in ms for the simulation,
# as well as the expected weight each spike will contain
n_neurons = 100
run_time = 8000
weight_to_spike = 2.0
# neural parameters of the ifcur model used to respond to injected spikes.
# (cell params for a synfire chain)
cell_params_lif = {'cm': 0.25, 'i_offset': 0.0, 'tau_m': 20.0, 'tau_refrac': 2.0, 
                   'tau_syn_E': 5.0, 'tau_syn_I': 5.0, 'v_reset': -70.0,
                   'v_rest': -65.0, 'v_thresh': -50.0}
# create synfire populations (if cur exp)
pop_forward = Frontend.Population(n_neurons, Frontend.IF_curr_exp,
                                  cell_params_lif, label='pop_forward')
pop_backward = Frontend.Population(n_neurons, Frontend.IF_curr_exp,
                                   cell_params_lif, label='pop_backward')
# create equiv of parrot popultions for closed loop calculation
pop_forward_parrot = Frontend.Population(
    n_neurons, Frontend.IF_curr_exp, cell_params_lif, label='pop_forward_parrot')
pop_backward_parrot = Frontend.Population(
    n_neurons, Frontend.IF_curr_exp, cell_params_lif, label='pop_backward_parrot')
# Create injection populations
injector_forward = Frontend.Population(
    2, ExternalDevices.SpikeInjector,
    {"port": 19344}, label='spike_injector_forward')
# Create a connection from the injector into the populations
Frontend.Projection(injector_forward, pop_forward,
                    Frontend.FromListConnector([(0, 0, weight_to_spike, 3)]))
Frontend.Projection(injector_forward, pop_backward,
                    Frontend.FromListConnector([(1, 99, weight_to_spike, 3)]))
# Synfire chain connections where each neuron is connected to its next neuron
# NOTE: there is no recurrent connection so that each chain stops once it
# reaches the end
loop_forward = list()
loop_backward = list()
for i in range(0, n_neurons - 1):
    loop_forward.append((i, (i + 1) % n_neurons, weight_to_spike, 3))
    loop_backward.append(((i + 1) % n_neurons, i, weight_to_spike, 3))
Frontend.Projection(pop_forward, pop_forward,
                    Frontend.FromListConnector(loop_forward))
Frontend.Projection(pop_backward, pop_backward,
                    Frontend.FromListConnector(loop_backward))
# Add links to the parrot populations for closed loop calculations
Frontend.Projection(pop_forward, pop_forward_parrot,
                    Frontend.OneToOneConnector(weight_to_spike, 1))
Frontend.Projection(pop_backward, pop_backward_parrot,
                    Frontend.OneToOneConnector(weight_to_spike, 1))
# record spikes from the synfire chains so that we can read off valid results
# in a safe way afterwards, and verify the behavior
pop_forward.record()
pop_backward.record()
# Activate the sending of live spikes for visualiser
ExternalDevices.activate_live_output_for(
    pop_forward, database_notify_host="localhost",
    database_notify_port_num=19996)
ExternalDevices.activate_live_output_for(
    pop_backward, database_notify_host="localhost",
    database_notify_port_num=19996)
# Activate the sending of spikes for the python reciever
ExternalDevices.activate_live_output_for(
    pop_forward_parrot, database_notify_host="localhost",
    database_notify_port_num=19995, port=13333)
ExternalDevices.activate_live_output_for(
    pop_backward_parrot, database_notify_host="localhost",
    database_notify_port_num=19995, port=13333)
# Create a condition to avoid overlapping prints
print_condition = Condition()
# Create a sender of packets for the forward population
def send_input_forward(label, sender):
    print_condition.acquire()
    print "Sending forward spike for neuron 0"
    print_condition.release()
    sender.send_spike(label, 0)
# Create a receiver of live spikes
def receive_spikes(label, time, neuron_ids):
    for neuron_id in neuron_ids:
        print_condition.acquire()
        print "Received spike at time", time, "from", label, "-", neuron_id
        print_condition.release()
        if neuron_id == 0 and label== "pop_backward_parrot":
            live_spikes_connection.send_spike("spike_injector_forward", 0)
        elif neuron_id == 99 and label== "pop_forward_parrot":
            live_spikes_connection.send_spike("spike_injector_forward", 1)
# Set up the live connection for sending spikes
live_spikes_connection = SpynnakerLiveSpikesConnection(
    local_port=19996, send_labels=["spike_injector_forward"])
# Set up the live connection for sending spikes to closed loop
live_spikes_connection_receiver = SpynnakerLiveSpikesConnection(
    receive_labels=["pop_forward_parrot", "pop_backward_parrot"],
    local_port=19995)
# Set up callbacks to occur at the start of simulation
live_spikes_connection.add_start_callback("spike_injector_forward",
                                          send_input_forward)
# Set up callbacks to occur when spikes are received
live_spikes_connection_receiver.add_receive_callback("pop_forward_parrot", receive_spikes)
live_spikes_connection_receiver.add_receive_callback("pop_backward_parrot", receive_spikes)
# Run the simulation on spiNNaker
Frontend.run(run_time)

# Retrieve spikes from the synfire chain population
spikes_forward = pop_forward.getSpikes()
spikes_backward = pop_backward.getSpikes()
# If there are spikes, plot using matplotlib
if len(spikes_forward) != 0 or len(spikes_backward) != 0:
    pylab.figure()
    if len(spikes_forward) != 0:
        pylab.plot([i[1] for i in spikes_forward],
                   [i[0] for i in spikes_forward], "b.")
    if len(spikes_backward) != 0:
        pylab.plot([i[1] for i in spikes_backward],
                   [i[0] for i in spikes_backward], "r.")
    pylab.ylabel('neuron id')
    pylab.xlabel('Time/ms')
    pylab.title('spikes')
    pylab.show()
else:
    print "No spikes received"
# Clear data structures on spiNNaker to leave the machine in a clean state for
# future executions
Frontend.end()
