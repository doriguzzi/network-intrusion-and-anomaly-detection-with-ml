# Network traffic feature extraction with Pyshark and Scapy
In these notebooks, we learn how to extract packet-level features from a pre-recorded network traffic trace of the [CIC-DDoS2019 dataset](https://www.unb.ca/cic/datasets/ddos-2019.html). This trace contains a mixture of benign and SYN Flood attack traffic.

We will use two popular tools, namely [Pyshark](https://github.com/KimiNewt/pyshark) and [Scapy](https://scapy.net/). We will also see how to capture live traffic from a network interface.