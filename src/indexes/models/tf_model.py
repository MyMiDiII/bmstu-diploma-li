import tensorflow as tf

from indexes.models.abs_model import AbstractModel
from indexes.metrics import MetricsCallback

from utils.keras_memory_usage import keras_model_memory_usage_in_bytes

class LossDiffStop(tf.keras.callbacks.Callback):
    def __init__(self, diff):
        super().__init__()
        self.diff = diff

    def on_epoch_end(self, epoch, logs=None):
        loss = logs['loss']
        if loss < self.diff:
            self.model.stop_training = True


class TFModel(AbstractModel):

    def __init__(self, model: tf.keras.Model):
        self.tf_model = model

    def build(self):
        self.tf_model.compile(optimizer=tf.keras.optimizers.SGD(1e-2),
                           loss=tf.keras.losses.MeanSquaredError(),
                           #loss=tf.keras.losses.MeanAbsoluteError(),
                           metrics=[])

    def train(self, keys, positions):
        self.metrics = MetricsCallback(keys, positions)

        self.tf_model.fit(
                keys,
                positions,
                batch_size=1,
                callbacks=[LossDiffStop(1e-3), self.metrics],
                epochs=30)

    def get_max_abs_err(self):
        return self.metrics.max_absolute_error

    def get_mean_abs_err(self):
        return self.metrics.mean_absolute_error

    def __call__(self, keys):
        return self.tf_model(keys)

    def size(self):
        return keras_model_memory_usage_in_bytes(self.tf_model, batch_size=32)

    def save(self, path):
        self.tf_model.save(path)

