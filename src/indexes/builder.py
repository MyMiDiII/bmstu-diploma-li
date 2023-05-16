import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf

from indexes.models.fcnn import FCNN
from indexes.models.rbf import RBN
from indexes.lindex import Lindex

class LindexBuilder:

    def __init__(self, model_name: str) -> Lindex:
        layer_neurons_num = 32
        b = 1 / np.sqrt(layer_neurons_num)
        a = -b
        initializer = tf.keras.initializers.RandomUniform(a, b)

        self.model = None
        print(model_name)
        match model_name:
            case "fcnn2":
                print("f2")
                self.model = FCNN([(layer_neurons_num, "relu", initializer)] * 2)

            case "fcnn3":
                print("f3")
                self.model = FCNN([(layer_neurons_num, "relu", initializer)] * 3)

            case "rbf":
                self.model = RBN()
                print("rbn")

    def build(self):
        return Lindex(self.model)

# draft
#rbf_initializer = InitCentersRandom(np.array([keys_variants[config["keys"]]]).T)
#rbf_initializer = None
