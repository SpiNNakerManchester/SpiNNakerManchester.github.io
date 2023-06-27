---
title: Changing board IP Addresses
---

**WARNING: Be very careful when setting IP addresses, as once set the new values will take effect!  If you loose the IP address after changing it or mis-type the IP address, there is no way to set it back again without connecting to the new IP address!**

**If you are changing the BMP IP Address and the SpiNNaker IP address, make sure you have one set and working before the other is changed!**

The bmpc application is part of the spinnaker_tools software available from:
[https://github.com/SpiNNakerManchester/spinnaker_tools](https://github.com/SpiNNakerManchester/spinnaker_tools).

To configure the bmp IP address:

```
bmp_ip <Flag.X> <MAC.M> <ip_addr.P> <gw_addr.P> <net_mask.P> <port.D>
```

To configure the SpiNNaker IP address:

```
spin_ip <Flag.X> <MAC.M> <ip_addr.P> <gw_addr.P> <net_mask.P> <port.D>
```

Where:

    - <Flag.X> is the flags to set in hex.  Normally these are c059 for spin_ip and c000 for the bmp_ip, but set them the same as they are already set if in doubt.
    - <MAC.M> is the MAC address as nn:nn:nn:nn:nn:nn.  Try to keep this from previous configurations.
    - <ip_addr.P> is the IP address as n.n.n.n.
    - <gw_addr.P> is the gateway IP address as n.n.n.n.
    - <net_mask.P> is the net mask as n.n.n.n.
    - <port.D> is the integer port number that SCAMP will listen on.  Normally this 17893 (changing it will likely break a lot of software).

You can get the current settings using the commands above without any 
arguments.  You should do this to get the flags and MAC address at least.
