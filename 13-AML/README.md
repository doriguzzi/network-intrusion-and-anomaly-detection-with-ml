# Adversarial Machine Learning attack against a DL-based NIDS

LUCID (Lightweight, Usable CNN in DDoS Detection) is a lightweight Deep Learning-based DDoS detection framework suitable for online resource-constrained environments, which leverages Convolutional Neural Networks (CNNs) to learn the behaviour of DDoS and benign traffic flows with both low processing overhead and attack detection time. 

More details on the architecture of LUCID and its performance in terms of detection accuracy and execution time are available in the following research paper:

R. Doriguzzi-Corin, S. Millar, S. Scott-Hayward, J. Martínez-del-Rincón and D. Siracusa, "Lucid: A Practical, Lightweight Deep Learning Solution for DDoS Attack Detection," in *IEEE Transactions on Network and Service Management*, vol. 17, no. 2, pp. 876-889, June 2020, doi: 10.1109/TNSM.2020.2971776.

## Laboratory
In this laboratory, you will train and tune LUCID using *Random Search* (the original LUCID's code implements *Grid Search*) and the training/validation sets available in the ```sample-dataset``` folder. In this regard, you will replace the lists of hyperparameters into distributions of integers of floating-point numbers (when possible). Moreover, limit the number of search iterations to 5.

Once the model is trained, test it using the test set available in the ```sample-dataset``` folder. This will allow you to check whether LUCID works well with unseen data.

Finally, you will test LUCID using live traffic. To this aim, you will use a traffic trace of benign and DDoS data traffic. Using this trace you will verify the ability of LUCID to segregate malicious from  benign traffic, but also assess its robustness to AML evasion attacks by introducing small perturbations to the network traffic of the trace.

The details on training, tuning and testing LUCID are presented in the next sections of this README. 


## Training

The LUCID CNN is implemented in script ```lucid_cnn.py```. The script executes a grid search throughout a set of hyperparameters and saves the model that maximises the accuracy on the validation set in ```h5``` format (hierarchical data format).

At each point in the grid (each combination of hyperparameters), the training continues until the maximum number of epochs is reached or after the loss has not decreased for 10 consecutive times. This value is defined with variable ```PATIENCE=10``` at the beginning of the script. Part of the hyperparameters is defined in the script as follows:

- **Learning rate**:  ```"learning_rate": [0.1,0.01],```
- **Batch size**: ```"batch_size": [1024,2048]```
- **Number of convolutional filters**: ```"kernels": [32,64]```
- **L1 and L2 Regularization**: ```"regularization" : [None,'l1']```
- **Dropout**: ```"dropout" : [None,0.5]```

### Command options

To execute the training process, the following parameters can be specified when using ```lucid_cnn.py```:

- ```-t```, ```--train```: Starts the training process and specifies the folder with the dataset
- ```-e```, ```--epochs```: Maximum number of training epochs for each set of hyperparameters (default=1000)
- ```-cv```,```--cross_validation```: Number of folds used to split the training data for cross-validation (accepted values: 0,2,3, etc., 0 is the default value that means no cross-validation). 


### The training process

To train LUCID, execute the following command:

```
python3 lucid_cnn.py --train ./sample-dataset/
```

This command trains LUCID over the grid of hyperparameters, maximum 1000 epochs for each point in the grid. The training process can stop earlier if no progress towards the minimum loss is observed for PATIENCE=10 consecutive epochs. The model which maximises the accuracy on the validation set is saved in ```h5``` format in the ```output``` folder, along with a ```csv``` file with the performance of the model on the validation set.  The name of the two files is the same (except for the extension) and is in the following format:

```
10t-10n-DOS2019-LUCID.h5
10t-10n-DOS2019-LUCID.csv
```

The values of the best hyperparameters are reported in the ```csv``` file:

|Model|Samples|Accuracy|F1Score|Hyper-parameters|Validation Set|
|-----|-------|--------|-------|----------------|--------------|
|DOS2019-LUCID|677|0.9261|0.9256|"{'batch_size': 1024, 'dropout': 0.5, 'kernels': 64, 'learning_rate': 0.1, 'regularization': None}"|./sample-dataset/10t-10n-DOS2019-dataset-val.hdf5|

along with prediction results obtained on the validation set, such as  accuracy and F1 score. The last column is the path to the validation set used to validate the best model.


## Testing

Testing means evaluating a trained model of LUCID with unseen data (data not used during the training and validation steps), such as the test set in the ```sample-dataset``` folder. For this process,  the ```lucid_cnn.py``` provides a different set of options:

- ```-p```, ```--predict```: Perform prediction on the test sets contained in a given folder specified with this option. The folder must contain files in ```hdf5``` format with the ```test``` suffix
- ```-m```, ```--model```: Model to be used for the prediction. The model in ```h5``` format produced with the training
- ```-i```, ```--iterations```: Repetitions of the prediction process (useful to estimate the average prediction time)

To test LUCID, run the following command:

```
python3 lucid_cnn.py --predict ./sample-dataset/ --model ./output/10t-10n-DOS2019-LUCID.h5
```

The output printed on the terminal and saved in a text file in the ```output``` folder in the following format:

|Model|Time|Packets|Samples|DDOS%|Accuracy|F1Score|TPR|FPR|TNR|FNR|Source|
|-----|----|-------|-------|-----|--------|-------|---|---|---|---|------|
|DOS2019-LUCID|0.016|3285|749|0.437|0.9947|0.9939|0.9909|0.0024|0.9976|0.0091|10t-10n-DOS2019-dataset-test.hdf5|

Where ```Time``` is the execution time on a test set.  The values of ```Packets``` and ```Samples``` are the the total number of packets and samples in the test set respectively. More precisely, ```Packets``` is the total amount of packets represented in the samples (traffic flows) of the test set. ```Accuracy```, ```F1```, ```PPV```  are classification accuracy, F1 and precision scores respectively, ```TPR```, ```FPR```, ```TNR```, ```FNR``` are the true positive, false positive, true negative and false negative rates respectively. 

The last column indicates the name of the test set used for the prediction test. Note that the script loads and process all the test sets in the folder specified with option ``` --predict``` (identified with the suffix ```test.hdf5```). This means that the output might consist of multiple lines, on for each test set. 

## Online Inference

Once trained, LUCID can perform inference on live network traffic or on pre-recorded traffic traces saved in ```pcap``` format. This operational mode is implemented in the ```lucid_cnn.py``` script and leverages on ```pyshark``` and ```tshark``` tools to capture the network packets from one of the network cards of the machine where the script is executed, or to extract the packets from a ```pcap``` file. In both cases, the script simulates an online deployment, where the traffic is collected for a predefined amount of time (```time_window```) and then sent to the neural network for classification.

Online inference can be started by executing ```lucid_cnn.py``` followed by one or more of these options: 

- ```-pl```, ```--predict_live```: Perform prediction on the network traffic sniffed from a network card or from a ```pcap``` file available on the file system. Therefore, this option must be followed by either the name of a network interface (e.g., ```eth0```) or the path to a ```pcap``` file (e.g., ```/home/user/traffic_capture.pcap```)
- ```-m```, ```--model```: Model to be used for the prediction. The model in ```h5``` format produced with the training
- ```-y```, ```--dataset_type```: One between ```DOS2017```, ```DOS2018``` and ```DOS2019``` in the case of ```pcap``` files from the UNB's datasets. This option is not used by LUCID for the classification task, but only to produce the classification statistics (e.g., accuracy, F1 score, etc,) by comparing the ground truth labels with the LUCID's output
- ```-a```, ```--attack_net```: Specifies the subnet of the attack network (e.g., ```192.168.0.0/24```). Like option ```dataset_type```, this is used to generate the ground truth labels. This option is used, along with option ```victim_net```, in the case of custom traffic or pcap file with IP address schemes different from those in the three datasets ```DOS2017```,  ```DOS2018``` or ```DOS2019``` 
- ```-y```, ```--victim_net```: The subnet of the victim network (e.g., ```10.42.0.0/24```), specified along with option ```attack_net``` (see description above).

### Inference on live traffic

If the argument of ```predict_live``` option is a network interface, LUCID will sniff the network traffic from that interface and will return the classification results every time the time window expires. The duration of the time window is automatically detected from the prefix of the model's name (e.g., ```10t``` indicates a 10-second time window). To start the inference on live traffic, use the following command:

```
python3 lucid_cnn.py --predict_live lo --model ./output/10t-10n-DOS2019-LUCID.h5
```

Where ```lo``` is the name of the loopback interface.
Once LUCID has been started using the command above, we can start the attack from another terminal using ```tcpreplay``````:

```
sudo tcpreplay -i lo --loop=100 ddos-chunk-short.pcap
```

In this script, ```lo``` refers to the egress network interface (the loopback interface in this lab), while ```--loop 100``` tells ```tcpreplay``` to send the traffic trace 100 from times.
In addition, the option ```--pps``` can be used to replay packets at a given packets/sec:

```
sudo tcpreplay -i lo --loop=100 --pps=5 ddos-chunk-short.pcap
```

### Inference on pcap files

Similar to the previous case on live traffic, inference on a pre-recorded traffic trace can be started with command:

```
python3 lucid_cnn.py --predict_live ./sample-dataset/ddos-chunk-short.pcap --model ./output/10t-10n-DOS2019-LUCID.h5
```

In this case, the argument of option ```predict_live``` must be the path to a pcap file. The script parses the file from the beginning to the end, printing the classification results every time the time window expires. The duration of the time window is automatically detected from the prefix of the model's name (e.g., ```10t``` indicates a 10-second time window). 