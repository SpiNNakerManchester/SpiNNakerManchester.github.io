---
title: The SpiNNaker software stack Buffer functionality. 
---

This page attempts to describe the functionality used by the SpiNNaker tool chain for buffering data in and out of a SpiNNaker machine during an executing application.

# What is the Buffer Manager

The buffer manager is a piece of code that resides in the [SpiNNFrontEndCommon](https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon) module. It supports the splitting of a block of data that is too large to store on the memory of the SpiNNaker chips themselves. This can either be for play back purposes (used by the sPyNNaker Front end for injecting spikes into a neural application during the simulation) or for storing results on chip for reliable extraction (such as state changes in computational nodes of an application). 

More information will follow.
