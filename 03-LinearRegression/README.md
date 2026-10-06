# Anomaly detection with Linear and Polynomial Regression
In this demonstration, we will use Linear and Polynomial Regression to predict real numbers. With synthetic data, we simulate the prediction of the average packet size of flows (dependent variable) using the time feature (independent variable). With these simulations, we can understand the properties of Linear and Polynomial Regression and visualise the problem of overfitting.
In addition, we use network traffic traces of benign and malicious data to train an anomaly detection system that predicts the average packet size of traffic flows. The resulting prediction is used to spot flows with anomalous average packet size. 

We will use a dataset of benign and two types of DDoS attacks: WebDDoS and DNS-based reflection DDoS attack. These attacks are part of the CIC-DDoS2019 dataset (https://www.unb.ca/cic/datasets/ddos-2019.html).
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


In this laboratory, we will instantiate a Linear and Polynomial Regression models and we will train them.
The notebook [LinearRegressionOneFeature.ipynb](./LinearRegressionOneFeature.ipynb) shows the different performance of Linear and Polynomial regression on synthetic data with non-linear data.
The notebook [LinearRegressionOneFeatureOverfitting.ipynb](./LinearRegressionOneFeatureOverfitting.ipynb) demonstrates the issue of overfitting the training data with high-degree Polynomial Regression.
The notebook [LinearRegressionDDoS.ipynb](./LinearRegressionDDoS.ipynb) implements a network anomaly detection with Linear and Polynomial Regression using pre-recorded network traffic traces.