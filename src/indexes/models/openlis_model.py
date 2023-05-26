import openlis
from openlis.data.data_set import DataSet
import openlis.model
import openlis.database
li = openlis
import numpy as np

from indexes.models.abs_model import AbstractModel

class OpenlisModel(AbstractModel):

    def __init__(self):
        pass

    def build(self):
        pass

    def train(self, keys, positions):
        data_set = DataSet(keys, positions)
        data_sets = li.data.create_train_validate_data_sets(data_set,
                                        validation_size=0)
        rmi = openlis.model.RMI_simple(data_sets.train,
                               hidden_layer_widths=[8,8],
                               num_experts=100)
        self.rmi_db = openlis.database.IndexStructurePacked(model=rmi)
        self.rmi_db.train(batch_sizes=[10000,1000],
             max_steps=[500,500],
             learning_rates=[0.001,1000],
             model_save_dir='tf_checkpoints_example')

    def __call__(self, keys):
        positions = self.rmi_db.select(keys)
        return positions

    def get_max_abs_err(self):
        return 0

    def get_mean_abs_err(self):
        return 0

    def size(self):
        return 0

    def save(self, path):
        pass
