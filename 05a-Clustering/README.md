# Clustering with K-means and DBSCAN
In this demonstration, we will test the k-means and DBSCAN algorithms with network traffic. Specifically, we will use such clustering techniques to group network flows into clusters in an unsupervised fashion.

We will use a dataset of benign and various DDoS attacks from the CIC-DDoS2019 dataset (https://www.unb.ca/cic/datasets/ddos-2019.html).
The network traffic has been previously pre-processed in a way that packets are grouped in bi-directional traffic flows using the 5-tuple (source IP, destination IP, source Port, destination Port, protocol). Each flow is represented with 21 packet-header features computed from max 1000 packets:

| Feature nr.         | Feature Name |
|---------------------|---------------------|
| 00 | timestamp (mean IAT) | 
| 01 | packet_length (mean)| 
| 02 | IP_ttl (mean) |
| 03 | IP_flags_df (sum) |
| 04 | IP_flags_mf (sum) |
| 05 | IP_flags_rb (sum) | 
| 06 | IP_frag_off (sum) |
| 07 | TCP_length (mean) |
| 08 | TCP_flags_ack (sum) |
| 09 | TCP_flags_cwr (sum) |
| 10 | TCP_flags_ece (sum) |
| 11 | TCP_flags_fin (sum) |
| 12 | TCP_flags_push (sum) |
| 13 | TCP_flags_reset (sum) |
| 14 | TCP_flags_syn (sum) |
| 15 | TCP_flags_urg (sum) |
| 16 | TCP_window_size (mean) |
| 17 | UDP_length (mean) |
| 18 | ICMP_type (mean) |
| 19 | ICMP_code (mean) |
| 20 | Packets (counter)|


The demonstration focusses on the k-means algorithms and shows a sample application of this clustering technique to network traffic flows of two different DDoS attacks. The demonstration also introduces the Adjusted Rand Index (ARI) accuracy metric to evaluate the performance of the clustering algorithm, and shows how to find the optimal number of clusters using the Elbow method.
