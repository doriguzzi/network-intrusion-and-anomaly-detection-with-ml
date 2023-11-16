# Copyright (c) 2022 @ FBK - Fondazione Bruno Kessler
# Author: Roberto Doriguzzi-Corin
# Project: LUCID: A Practical, Lightweight Deep Learning Solution for DDoS Attack Detection
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import h5py
import glob
from collections import OrderedDict


SEED = 1
MAX_FLOW_LEN = 10 # number of packets
TIME_WINDOW = 10
TRAIN_SIZE = 0.90 # size of the training set wrt the total number of samples

protocols = ['arp','data','dns','ftp','http','icmp','ip','ssdp','ssl','telnet','tcp','udp']
powers_of_two = np.array([2**i for i in range(len(protocols))])


def get_feature_list(time_window=10,max_flow_len=10):
    # feature list with min and max values
    feature_list = OrderedDict([
        ('timestamp', [0,time_window]),
        ('packet_length',[0,1<<16]),
        #('highest_layer',[0,1<<32]),
        ('IP_flags_df',[0,max_flow_len]),
        ('IP_flags_mf',[0,max_flow_len]),
        ('IP_flags_rb',[0,max_flow_len]),
        ('IP_frag_off',[0,1<<13]),
        ('protocols',[0,1<<len(protocols)]),
        ('TCP_length',[0,1<<16]),
        ('TCP_flags_ack',[0,max_flow_len]),
        ('TCP_flags_cwr',[0,max_flow_len]),
        ('TCP_flags_ece',[0,max_flow_len]),
        ('TCP_flags_fin',[0,max_flow_len]),
        ('TCP_flags_push',[0,max_flow_len]),
        ('TCP_flags_res',[0,max_flow_len]),
        ('TCP_flags_reset',[0,max_flow_len]),
        ('TCP_flags_syn',[0,max_flow_len]),
        ('TCP_flags_urg',[0,max_flow_len]),
        ('TCP_window_size',[0,1<<16]),
        ('UDP_length',[0,1<<16]),
        ('ICMP_type',[0,1<<8]),
        ('Packets',[0,10])]
    )
    return feature_list

def get_feature_names():
    features_names_list = get_feature_list().keys()
    return list(features_names_list)

def load_dataset(path,channels=False):
    filename = glob.glob(path)[0]
    dataset = h5py.File(filename, "r")
    set_x_orig = np.array(dataset["set_x"][:])  # features
    set_y_orig = np.array(dataset["set_y"][:])  # labels

    if channels == True:
        X_train = np.reshape(set_x_orig, (set_x_orig.shape[0], set_x_orig.shape[1], set_x_orig.shape[2], 1))
    else:
        X_train = set_x_orig
    Y_train = set_y_orig#.reshape((1, set_y_orig.shape[0]))

    return X_train, Y_train

def scale_linear_bycolumn(rawpoints, mins,maxs,high=1.0, low=0.0):
    rng = maxs - mins
    return high - (((high - low) * (maxs - rawpoints)) / rng)

def count_packets_in_dataset(X_list):
    packet_counters = []
    for X in X_list:
        packet_counters.append(int(np.sum(X[:,20])))

    return packet_counters

def all_same(items):
    return all(x == items[0] for x in items)

# min/max values of features based on the nominal min/max values of the single features (as defined in the feature_list dict)
def static_min_max(time_window=10,max_flow_len=10):
    feature_list = get_feature_list(time_window,max_flow_len)

    min_array = np.zeros(len(feature_list))
    max_array = np.zeros(len(feature_list))

    i=0
    for feature, value in feature_list.items():
        min_array[i] = value[0]
        max_array[i] = value[1]
        i+=1

    return min_array,max_array

# min/max values of features based on the values in the dataset
def find_min_max(X):
    sample_len = X[0].shape[0]
    max_array = np.zeros((1,sample_len))
    min_array = np.full((1, sample_len),np.inf)

    for feature in X:
        temp_feature = np.vstack([max_array,feature])
        max_array = np.amax(temp_feature,axis=0)
        temp_feature = np.vstack([min_array, feature])
        min_array = np.amin(temp_feature, axis=0)

    return min_array,max_array

def normalize_and_padding(X,mins,maxs,max_flow_len,padding=True):
    norm_X = []
    for sample in X:
        if sample.shape[0] > max_flow_len: # if the sample is bigger than expected, we cut the sample
            sample = sample[:max_flow_len,...]
        packet_nr = sample.shape[0] # number of packets in one sample

        norm_sample = scale_linear_bycolumn(sample, mins, maxs, high=1.0, low=0.0)
        np.nan_to_num(norm_sample, copy=False)  # remove NaN from the array
        if padding == True:
            norm_sample = np.pad(norm_sample, ((0, max_flow_len - packet_nr), (0, 0)), 'constant',constant_values=(0, 0))  # padding
        norm_X.append(norm_sample)
    return norm_X

def normalize(X,mins,maxs):
    norm_X = []
    for sample in X:
        norm_sample = scale_linear_bycolumn(sample, mins, maxs, high=1.0, low=0.0)
        np.nan_to_num(norm_sample, copy=False)  # remove NaN from the array
        norm_X.append(norm_sample)
    return norm_X

def padding(X,max_flow_len):
    padded_X = []
    for sample in X:
        flow_nr = sample.shape[0]
        padded_sample = np.pad(sample, ((0, max_flow_len - flow_nr), (0, 0)), 'constant',
                              constant_values=(0, 0))  # padding
        padded_X.append(padded_sample)
    return padded_X

def flatten_samples(X):
    X_new = []
    for sample in X:
        new_sample = []
        time_feature = np.mean(np.ediff1d(sample[:,0],to_begin=0)) #mean of the differences between consecutive elements of an array.
        new_sample.append(time_feature)
        packet_len = np.mean(sample[:,1])
        new_sample.append(packet_len)
        # highest_layer = np.mean(sample[:,2])
        # new_sample.append(highest_layer)
        ip_flags = list(np.sum(sample[:,2:5],axis=0)) # we take the sum of each flag
        new_sample = new_sample + ip_flags
        frag_off = np.mean(sample[:,5])
        new_sample.append(frag_off)
        protocols = np.mean(sample[:,6])
        new_sample.append(protocols)
        tcp_len = np.mean(sample[:,7])
        new_sample.append(tcp_len)
        tcp_flags = list(np.sum(sample[:,8:17],axis=0)) # we take the sum of each flag
        new_sample = new_sample + tcp_flags
        tcp_win_size = np.mean(sample[:,17])
        new_sample.append(tcp_win_size)
        udp_len = np.mean(sample[:,18])
        new_sample.append(udp_len)
        icmp_type = np.mean(sample[:,19])
        new_sample.append(icmp_type)
        packets_nr = sample.shape[0] #number of packets in the sample
        new_sample.append(packets_nr)

        new_sample = np.array(new_sample)
        X_new.append(new_sample)
    return X_new