---
title: Using 2D Convolutions with SpiNNaker
---

Populations in PyNN on SpiNNaker are typically 1-dimensional.  This can make handling of 2D data on the platform inefficient.  To address this, we now support the partitioning and placement of Populations in 2D on the master branches of the git repositories.  This means that connections between these Populations can be handled more efficiently, depending on that connectivity; in particular, convolutional connectivity is handled with a better division of labour between cores, and fewer unnecessary spike packets sent between cores.

In addition to the better routing of spike packets, the software updates also include better handling of the convolution processing itself.  In particular, the cores hold the kernel weights in local memory and apply them to the incoming data dynamically.  This avoids the need to transfer data from SDRAM, and so speeds up the processing significantly.

The SpiNNaker software current supports 2D representations and convolutions on the master branches of the git repositories.  These can be used if you have a local SpiNNaker board from the command line by following the instructions [here](gitinstall.html), or by using the sPyNNakerGit kernel on Jupyter [here](https://spinn-20.cs.man.ac.uk).

Once support is in place, 2D Populations can be used as in the following example:

    import spynnaker8 as p
    import numpy
    from pyNN.space import Grid2D

    # The rectangle of neurons per core
    SUB_WIDTH = 32
    SUB_HEIGHT = 16

    p.setup(1.0)

	# Set the number of neurons per core to a rectangle
	p.set_number_of_neurons_per_core(p.IF_curr_exp, (SUB_WIDTH, SUB_HEIGHT))

	# Make a kernel and convolution connector
	k_shape = numpy.array([5, 5], dtype='int32')
	k_size = numpy.prod(k_shape)
	kernel = (numpy.arange(k_size) - (k_size / 2)).reshape(k_shape) * 0.1
	conn = p.ConvolutionConnector(kernel)

	# Start with an input shape, and deduce the output shape
	in_shape = (11, 11)
	out_shape = conn.get_post_shape(in_shape)
	n_input = numpy.prod(in_shape)
	n_output = numpy.prod(out_shape)

	# Make a 2D source that spikes at the middle if the input shape
	spike_idx = ((in_shape[1] // 2) * in_shape[0]) + (in_shape[1] // 2)
	spike_times = [[1.0] if i == spike_idx else [] for i in range(n_input)]

	# Note the structure=Grid2D, which makes this a 2D population
	src = sim.Population(
	    n_input, sim.SpikeSourceArray, {'spike_times': spike_times},
	    label='input spikes', structure=Grid2D(in_shape[0] / in_shape[1]))

	# Make a 2D target Population and record it
    output = sim.Population(
	    n_output, sim.IF_curr_exp(), label="out",
       structure=Grid2D(out_shape[0] / out_shape[1]))
    output.record('v')

    # Connect the two populations with the convolution.  Note the use
    # of the synapse_type to ensure fast convolutional processing is
    # done
    p.Projection(src, output, conn, p.Convolution())

