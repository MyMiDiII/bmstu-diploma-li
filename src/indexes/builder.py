import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf

from indexes.models.tf_model import TFModel
from indexes.models.tf_models.fcnn import FCNN
from indexes.models.tf_models.rbf import RBN
from indexes.models.openlis_model import OpenlisModel
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
                fcnn = FCNN([(layer_neurons_num, "relu", initializer)] * 2)
                self.model = TFModel(fcnn)

            case "fcnn3":
                print("f3")
                fcnn = FCNN([(layer_neurons_num, "relu", initializer)] * 3)
                self.model = TFModel(fcnn)

            case "rbf":
                print("rbn")
                rbn = RBN(None)
                self.model = TFModel(rbn)

            case "openlis":
                self.model = OpenlisModel()


    def build(self):
        return Lindex(self.model)

# draft
#rbf_initializer = InitCentersRandom(np.array([keys_variants[config["keys"]]]).T)
#rbf_initializer = None
