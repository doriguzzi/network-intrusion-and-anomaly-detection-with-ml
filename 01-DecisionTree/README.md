# Decision Trees and accuracy metrics
In this demonstration, we will analyse the properties of Decision Trees (DTs) through a network traffic classification problem.
In particular, we will use a dataset of benign and four types of DDoS attacks: SYN Flood, UDP Lag, WebDDoS and and DNS-based reflection DDoS attack. These attacks are part of the CIC-DDoS2019 dataset (https://www.unb.ca/cic/datasets/ddos-2019.html).

The DT classifies the traffic into five classes (either benign or one of the attack classes) and the results are displayed using confusion matrices and common accuracy matrices.

The code of this demonstration is available in the following Jupyter notebook: [decision-tree-dos2019.ipynb](./decision-tree-dos2019.ipynb).

In addition, we will also test some regularisation techniques to avoid overfitting. In this case, we will consider a regression problem with a synthetic dataset:
[decision-tree-regression.ipynb](./decision-tree-regression.ipynb) 