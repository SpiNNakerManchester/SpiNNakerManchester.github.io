---
title: Executing the SpiNNaker software stack reload functionality. 
---

The SpiNNaker software stack's reload functionality supports the loading and executing of a already mapped application onto the same SpiNNaker machine without having to go through the mapping process again. 

# Caveats

The reload script has a bunch of functional caveats. There are:
 
1. The reload script does not run your entire python script, so any functionality between the p.end() and the end of your script will not be ran again; thus it is recommended that reload is used mainly for scripts which involve live input and output.
1. The reload script is a separate function, and so any calls made to plugins or none tool chain supported functions will not be repeated during rerun.
1. The reload script does not operate in conjunction with the auto_pause_and_resume functionality, and so you must have mapped your script with that functionality turned off.
1. The reload script will only reload and run up to the first call to run() in your script.  Subsequent calls to run() or calls to reset() will not be registered.

# How to you use the reload functionality.

When you run your script for the first time, you must ensure that your .cfg file has:

    [Reports]
    writeReloadSteps = True
    
and does not have:

    [Buffers]
    use_auto_pause_and_resume = True
    
Once the original script has ran, within the reports folder, there will be a script called rerun.py. To reload the script, all you need to do is run:

    ```python reload.py```

    
