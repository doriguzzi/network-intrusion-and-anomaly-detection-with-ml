# Network Intrusion and Anomaly Detection with Machine Learning
A series of lab sessions for the students of the course on Network Intrusion and Anomaly Detection with Machine Learning. 

The laboratories in this repository are based on Python and Jupyter notebooks (https://jupyter.org/). The Python environment can be configured by using the ```conda``` software environment (https://docs.conda.io/projects/conda/en/latest/).
We suggest the installation of ```miniconda```, a light version of ```conda```. ```miniconda``` is available for MS Windows, MacOSX and Linux and can be installed by following the guidelines available at https://docs.conda.io/en/latest/miniconda.html#. MS Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11 are required.
In MS Windows, first install the Windows subsystem for Linux from the command line: ```wsl.exe —install``` (see [here](https://learn.microsoft.com/en-us/windows/wsl/install) for more info). This command will install an Ubuntu Linux OS on your computer. You can access the Linux command line by executing the **WSL** app from the Windows menu, then follow the guidelines for the Linux OS below.


Open a terminal, execute one of the following commands (based on your operating system) and follow the on-screen instructions:

```
bash Miniconda3-latest-Linux-x86_64.sh (on Linux operating systems)
bash Miniconda3-latest-MacOSX-x86_64.sh (on macOS)
```

Then create a new ```conda``` environment (called ```python39```) based on Python 3.13.5:

```
conda create -n python313 python=3.13.5
```

Activate the new ```python313``` environment:

```
conda activate python313
```

And configure the environment with ```tensorflow``` and a few more packages:

```
(python39)$ pip install tensorflow==2.20
(python39)$ pip install scikit-learn h5py pyshark matplotlib jupyter graphviz pandas scikeras
```

<!-- On macOS (tested on Apple M1, M2 and M3 CPUs)
```
(python39)$ conda install -c conda-forge tensorflow=2.7.1 numpy=1.26.4
(python39)$ conda install -c conda-forge scikit-learn h5py pyshark matplotlib jupyter graphviz
``` -->
Pyshark is used in the ```lucid_dataset_parser.py``` script for data pre-processing.
Pyshark is just Python wrapper for tshark, meaning that ```tshark``` must be also installed. On an Ubuntu-based OS, use the following command:

```
sudo apt install tshark
```

In macOS, just download ```Wireshark``` from [here](https://www.wireshark.org/download.html) and install it.

Please note that the current parser code works with ```wireshark```/```tshark``` **version 4.4.9**.

## Executing the code
For Jupyter-based laboratories, first start Jupyter from the terminal:
```
(python39)$ jupyter notebook
```
Your browser should automatically open the notebook. Otherwise, copy and paste one of the links provided on the terminal. It should be something like:

```
Or copy and paste one of these URLs:
        http://localhost:8888/?token=f225f0f46d9e476ea4c80023f3244634db911c29dea3e3d0
     or http://127.0.0.1:8888/?token=f225f0f46d9e476ea4c80023f3244634db911c29dea3e3d0
```

Browse through the filesystem and click on the target notebook (a file with extension ```ipynb```).
In the case of pure Python code, please follow the instructions within the specific README of the laboratory.