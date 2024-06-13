---
title: PyNN on SpiNNaker Installation Guide
layout: default
published: true
---

This guide details how to install the release version of the tools required to run simulations on SpiNNaker using the PyNN scripting language, if you have a local SpiNNaker machine.
If you wish to run jobs on the million-core SpiNNaker machine in Manchester, then we suggest you use our [Jupyter Notebook](/latest/jupyter) instructions, or submit jobs via the [HBP Portal](/latest/hbp_portal) instead.

* [Operating Systems and Python](#Python)
* [Installation](#Installation)
* [Configuration](#Configuration)
* [Running some examples](#Examples)
* [Troubleshooting](#Trouble)

# <a name="Python"></a> Operating Systems and Python
To the best of our knowledge the spinnaker code runs on all current Linux, Windows and macOS systems as well as all current Python 3 version.

Full testing is done using Ununtu 22.04 and Python 3.12 so these are our recommendations.

Limited testing is done using Ubuntu-24.04, Ubuntu-20.04, Windows 10, Windows 11, macOS 11 and macOS 14 as well as Python versions 3.8, 3.9, 3.10, 3.11.

As the time of writing Python 3.13 could not be supported.

We always test using the latest version of our Python dependencies so recommend keeping all python packages up to date.

# <a name="Installation"></a> Installation
We recommend using a [virtual environment](https://virtualenv.pypa.io/en/latest/) as that makes is much easier to redo the installation later if things go wrong, and avoids conflicts with other python installations.

If you have not ready installed [virtual environment](https://virtualenv.pypa.io/en/latest/) please follow their installations instructions.

1. Activate your virtualenv, `<name>`

       source <name>/bin/activate

1. Uninstall the existing tools (if previously installed)

If you already have installed sPyNNaker previously (and the optional sPyNNakerExternalDevicesPlugin and/or sPyNNakerExtraModelsPlugin), you will need to uninstall it:

       pip uninstall pyNN-SpiNNaker
       pip uninstall sPyNNaker

1. Install Matplotlib:

       pip install matplotlib

1. Install sPyNNaker:

       pip install sPyNNaker

1. Install pyNN-SpiNNaker:

       python -m spynnaker.setup_pynn

# <a name="Configuration"></a> Configuration

When SpyNNaker is first called, if a configuration file is not found, it will create one in your home directory and exit.
It is possible to ask sPyNNaker to do this before you run your first simulation as follows:

Run this small script

    import pyNN.spiNNaker as sim
    sim.setup()
    sim.end()

Unless one already exists a new file called ".spynnaker.cfg" will be created in your home directory.  
You must edit this file to ensure that sPyNNaker can access your SpiNNaker machine.  
Upon opening this file, the part to alter will look like the following:
Warning some systems consider ".spynnaker.cfg" a hidden file.

```
[Machine]
machineName = None
version = None
```

If you have a SpiNNaker board, then go to [Local Board](#LocalBoard).

If you do not have a SpiNNaker board, then you have two options:

1) If you can directly access a local machine that uses spalloc (for example, at Manchester University and wish to use the million-core machine), then you need to set the following parameters in the ".spynnaker.cfg" you just created (e.g.):

```
[Machine]
spalloc_server = spinnaker.cs.man.ac.uk
spalloc_user = user.name@email.address
```

where you edit spalloc_server if you are using a different spalloc_server; editing spalloc_user is helpful for administrators of the machine to contact you if there are any problems, which is why we suggest using an email address.

OR 2) To run in virtual mode, please follow the instructions in [Instructions on how to use the different front ends in virtual mode](https://spinnakermanchester.github.io) and then go to [Running some examples](#Examples).

## <a name="LocalBoard"></a> Local Board

Within the file, you should set `machineName` to the IP address or hostname of your SpiNNaker machine, and `version` to the version of your SpiNNaker board; this will almost certainly be "`3`" for a 4-chip board or "`5`" on a 48-chip board. The default IP address for a spinn-3 board is `192.168.240.253` and the default IP address for a spinn-5 board is `192.168.240.1`.

Now go to [Network Configuration](#NetworkConfiguration).

## <a name="NetworkConfiguration"></a> Network Configuration

Go to the network settings for your computer and add or set an IPv4 entry with the following address for the adapter connected to the SpiNNaker board:

 1. IP address = `192.168.240.254`
 2. sub-mask = `255.255.255.0`
 3. default gateway = `0.0.0.0`


Optional: See [Algorithms](/common_pages/Algorithms.html) for how advanced users change change the algorithms used.

# <a name="Examples"></a> Running some examples
1. Download the examples:

    * https://github.com/SpiNNakerManchester/PyNNExamples

1. Go to the "examples" folder
1. Run:

       python va_benchmark.py

1. You will see the system go through a series of processes from partitioning, to placement, to routing and finally to loading and running.
1. Once the example has finished, you should see a graph that will look something like this:

   ![VABenchmarkSpikes](spynnaker/6.0.0/vabenchmark8_v6.png)

If you get the output above, you have successfully installed your system.

# <a name="Trouble"></a> Troubleshooting

<!--
1. If on Windows you experience the error:

       **UnicodeDecodeError: 'ascii' codec can't decode byte 0xb0 in position 1: ordinal not in range(128)**

   Then to solve it, edit `C:\Python27\Lib\mimetypes.py` and add these codes:

   ```python
   if sys.getdefaultencoding() != 'gbk':
       reload(sys)
       sys.setdefaultencoding('gbk')
   ```

   before the following line:

   ```python
   default_encoding = sys.getdefaultencoding()
   ```
-->
1. In OSX, if experiencing the following tkinter error:

       _tkinter.TclError: no display name and no $DISPLAY environment variable

    it may be solved by setting the backend for matplotlib. This can be done by editing the matplotlibrc file in the current working directory to read to ```backend: TkAgg```. This is usually found in `$DEV/lib/pythonXXX/site-packages/matplotlib/mpl-data/matplotlibrc`

    In a virtualenv, create a new file in the root directory ```.matplotlib/matplotlibrc``` that reads ```backend: TkAgg```. ([Sample matplotlibrc file](https://matplotlib.org/_static/matplotlibrc))

    If you are still having issues, you may also need to install [XQuartz](https://www.xquartz.org/).

2. In OSX, if you have problems during the installation of the `csa` package (a dependency of sPyNNaker; this problem cascades outwards) within your virtualenv, then use:

        MPLBACKEND=module://matplotlib.backends.backend_agg pip install sPyNNaker --user

    This overrides the matplotlib plotting backend _just during the installation phase,_ which is sufficient to get a working installation if you are not actively using matplotlib to do immediate plotting of the data.

# <a name="Links"></a> Other Links

Follow [SpiNNaker Extensions](/latest/PyNNOnSpiNNakerExtensions.html) to install extensions for building new neuron models.

