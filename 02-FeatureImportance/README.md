# Feature importance analysis with Random Forest
In this laboratory, we will use a Random Forest to evaluate the relative importance of the features of the training set. This technique is often used to get rid of irrelevant features before training. 

We will use a dataset of benign and four types of DDoS attacks: SYN Flood, UDP Lag, WebDDoS and and DNS-based reflection DDoS attack. These attacks are part of the CIC-DDoS2019 dataset (https://www.unb.ca/cic/datasets/ddos-2019.html).
The network traffic has been previously pre-processed in a way that packets are grouped in bi-directional traffic flows using the 5-tuple (source IP, destination IP, source Port, destination Port, protocol). Each flow is represented with 21 packet-header features computed from max 10 packets:

- timestamp (mean IAT)
- packet_length (mean)
- IP_flags_df (sum)
- IP_flags_mf (sum)
- IP_flags_rb (sum)
- IP_frag_off (sum)
- protocols (mean)
- TCP_length (mean)
- TCP_flags_ack (sum)
- TCP_flags_cwr (sum)
- TCP_flags_ece (sum)
- TCP_flags_fin (sum)
- TCP_flags_push (sum)
- TCP_flags_res (sum)
- TCP_flags_reset (sum)
- TCP_flags_syn (sum)
- TCP_flags_urg (sum)
- TCP_window_size (mean)
- UDP_length (mean)
- ICMP_type (mean)
- Packets (counter)





In this laboratory, we will instantiate a Random Forest model by also indicating relevant hyperparameters such as: **number of trees** that compose the forest and the **stopping criteria** (e.g., max_depth) and we will train it.
To validate the performance of the RF model and to tune the hyperparameters, we will use the OOB score, that is the accuracy of the RF on the out-of-bag (OOB) samples (the samples not selected in the bagging sampling process).

Then, we will plot the feature importance histogram, which shows how the different features contribute to the reduction of the Gini impurity.

Finally, we will use the trained RF model to classify unseen traffic samples.

The code of this laboratory is available in the following Jupyter notebook: [FeatureImportance.ipynb](./FeatureImportance.ipynb)