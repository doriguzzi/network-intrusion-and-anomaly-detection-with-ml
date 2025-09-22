# Feature importance analysis with Random Forest
In this laboratory, you will use a Random Forest to evaluate the relative importance of the features of the training set. This technique is often used to get rid of irrelevant features before training. 

You will use a dataset of benign and various DDoS attacks from the CIC-DDoS2019 dataset (https://www.unb.ca/cic/datasets/ddos-2019.html).
The network traffic has been previously pre-processed in a way that packets are grouped in bi-directional traffic flows using the 5-tuple (source IP, destination IP, source Port, destination Port, protocol). Each flow is represented with 21 packet-header features computed from max 1000 packets:

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


In this laboratory, you will instantiate a Random Forest model by also indicating relevant hyperparameters such as: **number of trees** that compose the forest and the **stopping criteria** (e.g., max_depth) and we will train it.
To validate the performance of the RF model and to tune the hyperparameters, you will use the OOB score, that is the accuracy of the RF on the out-of-bag (OOB) samples (the samples not selected in the bagging sampling process).

Then, you will plot the feature importance histogram, which shows how the different features contribute to the reduction of the Gini impurity.

Finally, you will use the trained RF model to classify unseen traffic samples.

The code of this laboratory is available in the following Jupyter notebook: [FeatureImportance-Lab.ipynb](./FeatureImportance-Lab.ipynb)

The notebook [FeatureImportance-Methods.ipynb](./FeatureImportance-Methods.ipynb) illustrates alternative techniques for evaluating feature importance, including Recursive Feature Elimination (RFE), Feature Reset, Permutation, and Partial Dependence Plots (PDP).
