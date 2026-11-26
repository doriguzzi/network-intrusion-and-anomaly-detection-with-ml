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


SEED=0
ROWS_PER_SAMPLE = 10

NORMALIZE = False
RANDOMIZE = False
SENSORS = ["LIT101","AIT402","AIT502"] # predictions on these sensors

DATASET_FOLDER = "./SWaT2015/"


def load_dataset(path,channels=False):
    filename = glob.glob(path)[0]
    dataset = h5py.File(filename, "r")
    set_x_orig = np.array(dataset["set_x"][:])  # features
    set_y_pred = np.array(dataset["set_y_pred"][:])  # labels
    set_y_bin = np.array(dataset["set_y_bin"][:])  # labels

    if channels == True:
        X_train = np.reshape(set_x_orig, (set_x_orig.shape[0], set_x_orig.shape[1], set_x_orig.shape[2], 1))
    else:
        X_train = set_x_orig

    return X_train, set_y_pred, set_y_bin