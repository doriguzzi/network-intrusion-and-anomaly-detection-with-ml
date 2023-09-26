# Network Intrusion and Anomaly Detection with Machine Learning
A series of lab sessions for the students of the course on Network Intrusion and Anomaly Detection with Machine Learning

The laboratories in this repository can be executed in the Virtual Machines (VMs) provided for the course. In these VMs, the Python environment and all the required libraries are already installed.

Alternatively, the same environment can be replicated on a computer. This can be done by using the ```conda``` software environment (https://docs.conda.io/projects/conda/en/latest/).
We suggest the installation of ```miniconda```, a light version of ```conda```. ```miniconda``` is available for MS Windows, MacOSX and Linux and can be installed by following the guidelines available at https://docs.conda.io/en/latest/miniconda.html#. 

Execute one of the following commands (based on your operating system) and follow the on-screen instructions:

```
bash Miniconda3-latest-Linux-x86_64.sh (on Linux operating systems)
bash Miniconda3-latest-MacOSX-x86_64.sh (on macOS)
```

Then create a new ```conda``` environment (called ```python39```) based on Python 3.9:

```
conda create -n python39 python=3.9
```

Activate the new ```python39``` environment:

```
conda activate python39
```

And configure the environment with ```tensorflow``` and a few more packages:

On Linux operating systems:
```
(python39)$ pip install tensorflow==2.7.1
(python39)$ pip install scikit-learn h5py pyshark protobuf==3.19.6
```

On macOS (tested on Apple M1 CPU)
```
(python39)$ conda install -c conda-forge tensorflow=2.7.1
(python39)$ conda install -c conda-forge scikit-learn h5py pyshark
```
Pyshark is used in the ```lucid_dataset_parser.py``` script for data pre-processing.
Pyshark is just Python wrapper for tshark, meaning that ```tshark``` must be also installed. On an Ubuntu-based OS, use the following command:

```
sudo apt install tshark
```

Please note that the current parser code works with ```tshark``` **version 3.2.3 or lower** or **version 3.6 or higher**. Issues have been reported when using intermediate releases such as 3.4.X.