# Network traffic feature extraction with Pyshark and Scapy
In these notebooks, we will learn how to use the Bag-of-Words technique to convert text data into numerical vectors that machine learning algorithms can understand. You can pactice BoW and  other feature preprocessing techniques with the notebook [FeatureExtractionPreprocessing](./FeatureExtractionPreprocessing.ipynb). 

Finally, we will learn how to use PCA to visualise the network flow samples in 2 and 3 dimensional spaces. To do so, we will reduce the dimension of the data points from 21 features (see the flow representation below) to 2 and 3 respectively.

We will use a sample dataset of benign and various DDoS attacks from the CIC-DDoS2019 dataset (https://www.unb.ca/cic/datasets/ddos-2019.html).
The network traffic has been previously pre-processed in a way that packets are grouped in bi-directional traffic flows using the 5-tuple (source IP, destination IP, source Port, destination Port, protocol). Each flow is represented with 21 packet-header features computed from max 10 packets:

| Features           | 
|---------------------|
| timestamp (mean IAT)  <br> packet_length (mean) <br> IP_flags_df (sum) <br> IP_flags_mf (sum) <br> IP_flags_rb (sum) <br> IP_frag_off (sum) <br> protocols (mean) <br> TCP_length (mean) <br> TCP_flags_ack (sum) <br> TCP_flags_cwr (sum) <br> TCP_flags_ece (sum) <br> TCP_flags_fin (sum) <br> TCP_flags_push (sum) <br> TCP_flags_res (sum) <br> TCP_flags_reset (sum) <br> TCP_flags_syn (sum) <br> TCP_flags_urg (sum) <br> TCP_window_size (mean) <br> UDP_length (mean) <br> ICMP_type (mean) <br> Packets (counter) <br> |