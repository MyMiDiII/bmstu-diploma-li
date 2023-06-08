import numpy as np
#import tensorflow as tf

from indexes.lindex import Lindex

class LindexBuilder:

    def __init__(self, model_name: str) -> Lindex:
        layer_neurons_num = 32
        b = 1 / np.sqrt(layer_neurons_num)
        a = -b
       # initializer = tf.keras.initializers.RandomUniform(a, b)

        self.model = None
        print(model_name)
        match model_name:
            case "fcnn2":
                pass
                #from indexes.models.tf_model import TFModel
                #from indexes.models.tf_models.fcnn import FCNN
                #fcnn = FCNN([(layer_neurons_num, "relu", initializer)] * 2)
                #self.model = TFModel(fcnn)

            case "fcnn3":
                pass
                #from indexes.models.tf_model import TFModel
                #from indexes.models.tf_models.fcnn import FCNN
                #fcnn = FCNN([(layer_neurons_num, "relu", initializer)] * 3)
                #self.model = TFModel(fcnn)

            case "rbf":
                pass
                #from indexes.models.tf_model import TFModel
                #from indexes.models.tf_models.rbf import RBN
                #rbn = RBN(None)
                #self.model = TFModel(rbn)

            case "openlis":
                pass
                #from indexes.models.openlis_model import OpenlisModel
                #self.model = OpenlisModel()

            case "fcnn2-pt":
                from indexes.models.pt_model import PTModel
                print("PTModel")
                self.model = PTModel(2)

            case "fcnn3-pt":
                from indexes.models.pt_model import PTModel
                self.model = PTModel(3)


    def build(self):
        print("BUILD RUN")
        return Lindex(self.model)

# draft
#rbf_initializer = InitCentersRandom(np.array([keys_variants[config["keys"]]]).T)
#rbf_initializer = None
