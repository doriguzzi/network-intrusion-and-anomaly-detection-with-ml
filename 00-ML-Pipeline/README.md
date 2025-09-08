# Training, testing and deploying an ML-based Network Intrusion Detection System

In this laboratory, you will train and test a Convolutional Neural Network (CNN) on a dataset of benign and DDoS network traffic. After 100 epochs, the trained model is saved on the hard disk in [*keras* format](https://www.tensorflow.org/guide/keras/serialization_and_saving). The accuracy of the resulting model, as well as the duration of the training process, depends on a range of variables, such as the model's hyper-parameters, the model's layers (fully connected, convolutional), the optimizer (e.g., SGD or Adam) and on the number of training epochs.    

Although all these parameters can be tuned with automated procedures, in this laboratory you will modify them manually to understand the impact of your changes on the training process and output.

Once the model is trained, you can test its performance on the test set o using pre-recorded network traffic.

This laboratory is based on the LUCID framework, whose code is available at https://github.com/doriguzzi/lucid-ddos and documented in the following research paper:

R. Doriguzzi-Corin, S. Millar, S. Scott-Hayward, J. Martínez-del-Rincón and D. Siracusa, "Lucid: A Practical, Lightweight Deep Learning Solution for DDoS Attack Detection," in *IEEE Transactions on Network and Service Management*, vol. 17, no. 2, pp. 876-889, June 2020, doi: 10.1109/TNSM.2020.2971776.

## Training and testing
The training methods are implemented in the Jupyter notebook [training-binary.py](./training-binary.ipynb). After 100 epochs, the script produces a trained CNN in *keras* format saved in the ```output``` folder.

The training process is performed by using the training and validation set available in the ```sample-dataset``` folder. Some relevant hyperparameters of the model (number of convolutional kernels and their height) and of the training process (batch size, learning rate and max epochs) can be changed to improve the performance of the CNN.

One trained, the model can be tested on the test set through the Jupyter notebook [classify.ipynp](./classify.ipynb)

## Simulated deployment
Once trained, the CNN can perform inference on live network traffic or on pre-recorded traffic traces saved in ```pcap``` format. This operational mode is implemented in the ```lucid_cnn.py``` script and leverages on ```pyshark``` and ```tshark``` tools to extract the packets from a ```pcap``` file. The script simulates an online deployment, where the traffic is collected for a predefined amount of time (```time_window```) and then sent to the neural network for classification.

Inference on a pre-recorded traffic trace can be started with command:

```
python3 lucid_cnn.py --predict_live ./sample-dataset/CIC-DDoS-2019-UDPLag.pcap --model ./output/10t-10n-DOS2019-LUCID.keras --dataset_type DOS2019
```

The script parses the pcap file with the pre-recorded network traffic from the beginning to the end, printing the classification results every 10 seconds (default time window).