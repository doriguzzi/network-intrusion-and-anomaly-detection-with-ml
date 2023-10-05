# Anomaly detection with Linear and Polynomial Regression
In this laboratory, we will use Linear and Polynomial Regression to predict real numbers. With synthetic data, we simulate the prediction of the average packet size of flows (dependent variable) using the time feature (independent variable). With these simulations, we can understand the properties of Linear and Polynomial Regression and visualise the problem of overfitting.
In addition, we use network traffic traces of benign and malicious data to train an anomaly detection system that predicts the average packet size of traffic flows. The resulting prediction is used to spot flows with anomalous average packet size. 

We will use a dataset of benign and two types of DDoS attacks: WebDDoS and DNS-based reflection DDoS attack. These attacks are part of the CIC-DDoS2019 dataset (https://www.unb.ca/cic/datasets/ddos-2019.html).
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


In this laboratory, we will instantiate a Linear and Polynomial Regression models and we will train them.
The notebook [LinearRegressionOneFeature.ipynb](./LinearRegressionOneFeature.ipynb) shows the different performance of Linear and Polynomial regression on synthetic data with non-linear data.
The notebook [LinearRegressionOneFeatureOverfitting.ipynb](./LinearRegressionOneFeatureOverfitting.ipynb) demonstrates the issue of overfitting the training data with high-degree Polynomial Regression.
The notebook [LinearRegression.ipynb](./LinearRegression.ipynb) implements a network anomaly detection with Linear and Polynomial Regression using pre-recorded network traffic traces.