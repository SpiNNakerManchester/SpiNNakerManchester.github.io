# imports of both spynnaker and external device plugin.
import spynnaker.pyNN as Frontend
import spynnaker_external_devices_plugin.pyNN as ExternalDevices

#######################
# import to allow prefix type for the prefix eieio protocol
######################
from spynnaker_external_devices_plugin.pyNN.connections\
    .spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection

# plotter in python
import pylab
from multiprocessing import freeze_support
import Tkinter as tk


class PyNNScript(object):
    """
    the class which contains the pynn script
    """

    def __init__(self):

        # initial call to set up the front end (pynn requirement)
        Frontend.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)

        # neurons per population and the length of runtime in ms for the
        # simulation, as well as the expected weight each spike will contain
        self.n_neurons = 100
        run_time = 100000
        weight_to_spike = 2.0

        # neural parameters of the IF_curr model used to respond to injected
        # spikes.
        # (cell params for a synfire chain)
        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0
                           }

        ##################################
        # Parameters for the injector population.  This is the minimal set of
        # parameters required, which is for a set of spikes where the key is
        # not important.  Note that a virtual key *will* be assigned to the
        # population, and that spikes sent which do not match this virtual key
        # will be dropped; however, if spikes are sent using 16-bit keys, they
        # will automatically be made to match the virtual key.  The virtual
        # key assigned can be obtained from the database.
        ##################################
        cell_params_spike_injector = {

            # The port on which the spiNNaker machine should listen for
            # packets. Packets to be injected should be sent to this port on
            # the spiNNaker machine
            'port': 12345
        }

        ##################################
        # Parameters for the injector population.  Note that each injector
        # needs to be given a different port.  The virtual key is assigned
        # here, rather than being allocated later.  As with the above, spikes
        # injected need to match this key, and this will be done automatically
        # with 16-bit keys.
        ##################################
        cell_params_spike_injector_with_key = {

            # The port on which the spiNNaker machine should listen for
            # packets. Packets to be injected should be sent to this port on
            # the spiNNaker machine
            'port': 12346,

            # This is the base key to be used for the injection, which is used
            # to allow the keys to be routed around the spiNNaker machine.
            # This assignment means that 32-bit keys must have the high-order
            # 16-bit set to 0x7; This will automatically be prepended to
            # 16-bit keys.
            'virtual_key': 0x70000
        }

        # create synfire populations (if cur exp)
        pop_forward = Frontend.Population(
            self.n_neurons, Frontend.IF_curr_exp,
            cell_params_lif, label='pop_forward')
        pop_backward = Frontend.Population(
            self.n_neurons, Frontend.IF_curr_exp,
            cell_params_lif, label='pop_backward')

        # Create injection populations
        injector_forward = Frontend.Population(
            self.n_neurons, ExternalDevices.SpikeInjector,
            cell_params_spike_injector_with_key,
            label='spike_injector_forward')
        injector_backward = Frontend.Population(
            self.n_neurons, ExternalDevices.SpikeInjector,
            cell_params_spike_injector, label='spike_injector_backward')

        # Create a connection from the injector into the populations
        Frontend.Projection(
            injector_forward, pop_forward,
            Frontend.OneToOneConnector(weights=weight_to_spike))
        Frontend.Projection(
            injector_backward, pop_backward,
            Frontend.OneToOneConnector(weights=weight_to_spike))

        # Synfire chain connections where each neuron is connected to its next
        # neuron
        # NOTE: there is no recurrent connection so that each chain stops once
        # it reaches the end
        loop_forward = list()
        loop_backward = list()
        for i in range(0, self.n_neurons - 1):
            loop_forward.append((i, (i + 1) %
                                 self.n_neurons, weight_to_spike, 3))
            loop_backward.append(((i + 1) %
                                  self.n_neurons, i, weight_to_spike, 3))
        Frontend.Projection(pop_forward, pop_forward,
                            Frontend.FromListConnector(loop_forward))
        Frontend.Projection(pop_backward, pop_backward,
                            Frontend.FromListConnector(loop_backward))

        # record spikes from the synfire chains so that we can read off valid
        # results in a safe way afterwards, and verify the behavior
        pop_forward.record()
        pop_backward.record()

        # Activate the sending of live spikes
        ExternalDevices.activate_live_output_for(
            pop_forward, database_notify_host="localhost",
            database_notify_port_num=19996)
        ExternalDevices.activate_live_output_for(
            pop_backward, database_notify_host="localhost",
            database_notify_port_num=19996)

        # set up gui
        from multiprocessing import Process
        p = Process(target=GUI, args=[self.n_neurons])
        p.start()
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

        # Clear data structures on spiNNaker to leave the machine in a clean
        # state for future executions
        Frontend.end()
        p.join()


class GUI(object):
    """
    simple gui to demostrate live inejction of the spike io script.
    """

    def __init__(self, n_neurons):
        """
        creates the gui
        :return:
        """
        self._started = False
        # Set up the live connection for sending and receiving spikes
        self.live_spikes_connection = SpynnakerLiveSpikesConnection(
            receive_labels=None, local_port=19996,
            send_labels=["spike_injector_forward", "spike_injector_backward"])

        # Set up callbacks to occur at the start of simulation
        self.live_spikes_connection.add_start_callback(
            "spike_injector_forward", self.send_input_forward)
        root = tk.Tk()
        root.title("Injecting Spikes GUI")
        label = tk.Label(root, fg="dark green")
        label.pack()
        neuron_id_value = tk.IntVar()
        self.neuron_id = tk.Spinbox(
            root, from_=0, to=n_neurons - 1, textvariable=neuron_id_value)
        self.neuron_id.pack()
        pop_label_value = tk.StringVar()
        self.pop_label = tk.Spinbox(
            root, textvariable=pop_label_value,
            values=("spike_injector_forward", "spike_injector_backward"))
        self.pop_label.pack()
        button = tk.Button(root, text='Inject', width=25,
                           command=self.inject_spike)
        button.pack()
        root.mainloop()

    # Create a sender of packets for the forward population
    def send_input_forward(self, pop_label, _):
        """
        records that stuff has started on the spinnaker machine
        :param pop_label: label
        :param _: dont care
        :return:
        """
        self._started = True

    # add a gui with a button and scroll list
    def inject_spike(self):
        """
        is set off when inject is pressed, takes the vlaues from the spin
        boxes and fires a spike in.
        :return:
        """
        print "injecting with neuron_id {} to pop {}".format(
            self.neuron_id.get(), self.pop_label.get())
        if self._started:
            self.live_spikes_connection.send_spike(str(self.pop_label.get()),
                                                   int(self.neuron_id.get()))

# set up the initial script
if __name__ == '__main__':
    freeze_support()
    script = PyNNScript()
