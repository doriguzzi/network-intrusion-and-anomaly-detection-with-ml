# Copyright (c) 2025 @ FBK - Fondazione Bruno Kessler
# Author: Roberto Doriguzzi-Corin
# Project: LUCX: LUCID network traffic parser eXtended
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

import re
import numpy as np
import h5py
import glob
from sklearn.feature_extraction.text import CountVectorizer
from collections import OrderedDict


SEED = 1
MAX_FLOW_LEN = 10 # number of packets
TIME_WINDOW = 10
TRAIN_SIZE = 0.90 # size of the training set wrt the total number of samples

# Categorical feature possible values
categorical_features = dict(
    protocols = ['arp','data','dns','ftp','http','icmp','ip','ssdp','ssl','telnet','tcp','udp'],# 'tls_record_versions' : ['0x0300','0x0301','0x0302','0x0303','0x0304']
    ip_flags = ['df','mf','rb'],
    tcp_flags = ['ack','cwr','ece','fin','push','reset','syn','urg']
)
tls_categorical_features = dict(
tls_record_versions = ['0x0300','0x0301','0x0302','0x0303','0x0304'],
tls_handshake_extensions_supported_version = ['0x0300','0x0301','0x0302','0x0303','0x0304'],
tls_handshake_types = ['0x00','0x01','0x02','0x0b','0x0c','0x0d','0x0e','0x0f','0x10','0x14','0x15','0x16','0x17','0x18','0x19','0x1a','0xfe'],
tls_handshake_ciphersuites = ['0xC02F','0xC02B','0xC030','0xC02C','0x1301','0x1302','0x1303','0x1304','0x1305', '0x002F', '0x0035', '0x009C', '0x0000'],
tls_record_content_type = ['0x14','0x15','0x16','0x17','0x18']
)


def get_feature_list_flatten(time_window=10,max_flow_len=10,enable_tls=False):
    # feature list with min and max values
    feature_list = OrderedDict([
        ('timestamp', [0,time_window]),
        ('packet_length',[0,1<<16]),
        ('IP_ttl',[1,255]),
        ('IP_flags_df',[0,max_flow_len]),
        ('IP_flags_mf',[0,max_flow_len]),
        ('IP_flags_rb',[0,max_flow_len]),
        ('IP_frag_off',[0,1<<13])])
    for cat in categorical_features['protocols']:
        feature_list["protocols_" + str(cat)] = [0,max_flow_len]
    feature_list.update([
        ('TCP_length',[0,1<<16]),
        ('TCP_flags_ack',[0,max_flow_len]),
        ('TCP_flags_cwr',[0,max_flow_len]),
        ('TCP_flags_ece',[0,max_flow_len]),
        ('TCP_flags_fin',[0,max_flow_len]),
        ('TCP_flags_push',[0,max_flow_len]),
        ('TCP_flags_reset',[0,max_flow_len]),
        ('TCP_flags_syn',[0,max_flow_len]),
        ('TCP_flags_urg',[0,max_flow_len]),
        ('TCP_window_size',[0,1<<16])])
    if enable_tls:
        for feature_type in tls_categorical_features.keys():
            for cat in tls_categorical_features[feature_type]:
                feature_list[feature_type + "_" + str(cat)] = [0,max_flow_len]
        feature_list.update([
            ('TLS_record_length',[0,1<<14])]) # max TLS record length is 2^14 = 16384
    feature_list.update([
        ('UDP_length',[0,1<<16]),
        ('ICMP_type',[0,1<<8]),
        ('ICMP_code',[0,1<<8]),
        ('Packets',[0,max_flow_len])]
    )
    return feature_list

def get_feature_list_array(time_window=10,max_flow_len=10,enable_tls=False):
    # feature list with min and max values
    feature_list = OrderedDict([
        ('timestamp', [0,time_window]),
        ('packet_length',[0,1<<16]),
        ('IP_ttl',[1,255]),
        ('IP_flags_df',[0,1]),
        ('IP_flags_mf',[0,1]),
        ('IP_flags_rb',[0,1]),
        ('IP_frag_off',[0,1<<13])])
    for cat in categorical_features['protocols']:
        feature_list["protocols_" + str(cat)] = [0,1]
    feature_list.update([
        ('TCP_length',[0,1<<16]),
        ('TCP_flags_ack',[0,1]),
        ('TCP_flags_cwr',[0,1]),
        ('TCP_flags_ece',[0,1]),
        ('TCP_flags_fin',[0,1]),
        ('TCP_flags_push',[0,1]),
        ('TCP_flags_reset',[0,1]),
        ('TCP_flags_syn',[0,1]),
        ('TCP_flags_urg',[0,1]),
        ('TCP_window_size',[0,1<<16])])
    if enable_tls:
        for feature_type in tls_categorical_features.keys():
            for cat in tls_categorical_features[feature_type]:
                feature_list[feature_type + "_" + str(cat)] = [0,1]
        feature_list.update([
            ('TLS_record_length',[0,1<<14])]) # max TLS record length is 2^14 = 16384
    feature_list.update([
        ('UDP_length',[0,1<<16]),
        ('ICMP_type',[0,1<<8]),
        ('ICMP_code',[0,1<<8])]
    )
    return feature_list

def get_feature_names(flatten,enable_tls=False):
    if flatten == True:
        features_names_list = get_feature_list_flatten(enable_tls).keys()
    else:
        features_names_list = get_feature_list_array(enable_tls).keys()
    return list(features_names_list)

# Bag of Words encoding for categorical features
# Build lookup tables for one-hot encodings of all categories.
def precompute_encodings(features_dict,category=None):
    encodings = {}
    if category is not None:
        vocab = features_dict[category]
        encodings = {
            token: np.eye(len(vocab), dtype=int)[i]
            for i, token in enumerate(vocab)
        }
    else:
        for category, vocab in features_dict.items():
            encodings[category] = {
                token: np.eye(len(vocab), dtype=int)[i]
                for i, token in enumerate(vocab)
            }
    return encodings

# Split a sentence into words regardless of separator. 
def split_sentence(sentence):

    # Split on any sequence of non-alphanumeric characters
    words = re.split(r'\W+', sentence)
    
    # Remove empty strings
    return [w for w in words if w]

def sentence_to_encoding(sentence, encoding_lookup):
    encoding = []
    tokens = split_sentence(sentence)
    for token in tokens:
        if encoding_lookup.get(token) is not None:
            encoding.append(encoding_lookup[token])
    if not encoding:
        encoding.append(np.zeros(len(next(iter(encoding_lookup.values()))), dtype=int))
    
    total = np.sum(encoding, axis=0)
    return (total > 0).astype(int)


# Convert a list of 0s and 1s into a hexadecimal string
def bits_to_hex(bits):
    bit_string = ''.join(str(b) for b in bits)
    
    # Convert binary string to integer
    value = int(bit_string, 2)
    
    # Convert integer to hex
    return value

def load_dataset(path,channels=False):
    filename = glob.glob(path)[0]
    dataset = h5py.File(filename, "r")
    set_x_orig = np.array(dataset["set_x"][:])  # features-
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

def count_packets_in_dataset(X_list, flatten=True):
    packet_counters = []
    for X in X_list:
        if (flatten == False):
            TOT = X.sum(axis=2)
            packet_counters.append(np.count_nonzero(TOT))
        else:
            packet_counters.append(int(np.sum(X[:,-1])))

    return packet_counters

def all_same(items):
    return all(x == items[0] for x in items)

# min/max values of features based on the nominal min/max values of the single features (as defined in the feature_list dict)
def static_min_max(flatten, time_window=10,max_flow_len=10,enable_tls=False):
    if flatten == True:
        feature_list = get_feature_list_flatten(time_window,max_flow_len,enable_tls)
    else:
        feature_list = get_feature_list_array(time_window,max_flow_len,enable_tls)

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
    stacked_X = np.vstack(X)
    sample_len = stacked_X.shape[-1]
    max_array = np.zeros(sample_len)
    min_array = np.zeros(sample_len)

    for i in range(stacked_X.shape[-1]): # iterate over the columns (features)
        feature = stacked_X[:,i]
        max_array[i] = np.amax(feature)
        min_array[i] = np.amin(feature)
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

def flatten_samples(X,enable_tls=False):
    X_new = []
    protocols_len = len(categorical_features['protocols'])
    tls_cat_fields_count =  sum(len(v) for v in tls_categorical_features.values()) 

    for sample in X:
        new_sample = []
        f_index = 0 # feature index
        time_feature = np.mean(np.ediff1d(sample[:,f_index],to_begin=0)) #mean of the differences between consecutive elements of an array.
        new_sample.append(time_feature)
        f_index += 1
        packet_len = np.mean(sample[:,f_index])
        new_sample.append(packet_len)
        f_index += 1
        ttl = np.mean(sample[:,f_index])
        new_sample.append(ttl)
        f_index += 1
        ip_flags = list(np.sum(sample[:,f_index:f_index+3],axis=0)) # we take the sum of each flag
        new_sample = new_sample + ip_flags
        f_index += 3
        frag_off = np.mean(sample[:,f_index])
        new_sample.append(frag_off)
        f_index += 1
        protocols = list(np.sum(sample[:,f_index:f_index + protocols_len],axis=0)) # we take the sum of each flag
        new_sample = new_sample + protocols
        f_index += protocols_len
        tcp_len = np.mean(sample[:,f_index])
        new_sample.append(tcp_len)
        f_index += 1
        tcp_flags = list(np.sum(sample[:,f_index:f_index+8],axis=0)) # we take the sum of each flag
        new_sample = new_sample + tcp_flags
        f_index += 8
        tcp_win_size = np.mean(sample[:,f_index])
        new_sample.append(tcp_win_size)
        f_index += 1
        if enable_tls:
            tls_cat_fields = list(np.sum(sample[:,f_index:f_index+tls_cat_fields_count],axis=0)) # we take the sum of each field
            new_sample = new_sample + tls_cat_fields
            f_index += tls_cat_fields_count
            tls_record_len = np.mean(sample[:,f_index])
            new_sample.append(tls_record_len)
            f_index += 1
        udp_len = np.mean(sample[:,f_index])
        new_sample.append(udp_len)
        f_index += 1
        icmp_type = np.mean(sample[:,f_index])
        new_sample.append(icmp_type)
        f_index += 1
        icmp_code = np.mean(sample[:,f_index])
        new_sample.append(icmp_code)
        f_index += 1
        packets_nr = sample.shape[0] #number of packets in the sample
        new_sample.append(packets_nr)

        new_sample = np.array(new_sample)
        X_new.append(new_sample)
    return X_new