from pacman.model.abstract_classes.abstract_virtual_vertex import \
    AbstractVirtualVertex
from spinn_front_end_common.abstract_models\
    .abstract_outgoing_edge_same_contiguous_keys_restrictor import \
    AbstractOutgoingEdgeSameContiguousKeysRestrictor
from pacman.model.constraints.key_allocator_constraints\
    .key_allocator_fixed_key_and_mask_constraint \
    import KeyAllocatorFixedKeyAndMaskConstraint
from pacman.model.routing_info.key_and_mask import KeyAndMask


class MyExternalDevice(AbstractVirtualVertex,
                       AbstractOutgoingEdgeSameContiguousKeysRestrictor):

    def __init__(self, machine_time_step, timescale_factor, spikes_per_second,
                 ring_buffer_sigma, n_neurons, label,
                 spinnaker_link_id):

        if n_neurons != 20:
            print "Warning, this device has 20 neurons"

        AbstractVirtualVertex.__init__(self, n_neurons, spinnaker_link_id,
                                       label, n_neurons)
        AbstractOutgoingEdgeSameContiguousKeysRestrictor.__init__(self)

    def get_outgoing_edge_constraints(self, partitioned_edge, graph_mapper):
        constraints = AbstractOutgoingEdgeSameContiguousKeysRestrictor\
            .get_outgoing_edge_constraints(
                self, partitioned_edge, graph_mapper)
        constraints.append(KeyAllocatorFixedKeyAndMaskConstraint(
            [KeyAndMask(0x42000000, 0xFFFF0000)]))
        return constraints

    def is_virtual_vertex(self):
        return True

    def model_name(self):
        return "My External Device"


import pyNN.spiNNaker as p
from pacman.model.partitionable_graph.multi_cast_partitionable_edge \
    import MultiCastPartitionableEdge


p.setup(1.0)

device = p.Population(20, MyExternalDevice, {"spinnaker_link_id": 0},
                      label="external device")
pop = p.Population(20, p.IF_curr_exp, {}, label="population")
p.Projection(device, pop, p.OneToOneConnector())

p.run(10)
