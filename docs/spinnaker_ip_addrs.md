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

You can get the current settings using the commands above without any 
arguments.
