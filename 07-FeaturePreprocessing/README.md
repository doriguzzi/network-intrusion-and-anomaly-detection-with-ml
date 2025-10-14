# Feature extraction and preprocessing
In these notebooks, we will first demonstrate how Ensemble Learning techniques can mitigate the poor performance of shallow machine learning models on imbalanced training data ([EnsembleLearning](./EnsembleLearning.ipynb)).

Then, we will learn how to use the Bag-of-Words technique to convert text data into numerical vectors that machine learning algorithms can understand. You can practice BoW and  other feature preprocessing techniques with the notebook [FeatureExtractionPreprocessing](./FeatureExtractionPreprocessing.ipynb). 

Finally, we will learn how to use PCA to visualise the network flow samples in 1, 2 and 3 dimensional spaces. To do so, we will reduce the dimension of the data points from 21 features (see the flow representation below) to 1, 2 and 3 respectively ([PCA](./PCA.ipynb)).

We will use a sample dataset of benign and various DDoS attacks from the CIC-DDoS2019 dataset (https://www.unb.ca/cic/datasets/ddos-2019.html).
The network traffic has been previously pre-processed in a way that packets are grouped in bi-directional traffic flows using the 5-tuple (source IP, destination IP, source Port, destination Port, protocol). Each flow is represented with 21 packet-header features computed from max 10 packets:

| Feature nr.         | Feature Name |
|---------------------|---------------------|
| 00 | timestamp (mean IAT) | 
| 01 | packet_length (mean)| 
| 02 | IP_flags_df (sum) |
| 03 | IP_flags_mf (sum) |
| 04 | IP_flags_rb (sum) | 
| 05 | IP_frag_off (sum) |
| 06 | protocols (mean) |
| 07 | TCP_length (mean) |
| 08 | TCP_flags_ack (sum) |
| 09 | TCP_flags_cwr (sum) |
| 10 | TCP_flags_ece (sum) |
| 11 | TCP_flags_fin (sum) |
| 12 | TCP_flags_push (sum) |
| 13 | TCP_flags_res (sum) |
| 14 | TCP_flags_reset (sum) |
| 15 | TCP_flags_syn (sum) |
| 16 | TCP_flags_urg (sum) |
| 17 | TCP_window_size (mean) |
| 18 | UDP_length (mean) |
| 19 | ICMP_type (mean) |
| 20 | Packets (counter)|