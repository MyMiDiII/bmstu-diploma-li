from keras import backend as K
from tensorflow.keras.layers import Layer
from keras.initializers import RandomUniform, Initializer, Constant
import numpy as np
import tensorflow as tf


class InitCentersRandom(Initializer):
    def __init__(self, X):
        self.X = X

    def __call__(self, shape, dtype=None):
        idx = np.random.randint(self.X.shape[0], size=shape[0])
        return self.X[idx, :]


class RBFLayer(Layer):
    def __init__(self, output_dim, initializer=None, betas=1.0, **kwargs):
        self.output_dim = output_dim
        self.init_betas = betas
        self.initializer = initializer if initializer else RandomUniform(0.0, 1.0)

        super(RBFLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.centers = self.add_weight(name='centers',
                                       shape=(self.output_dim, input_shape[1]),
                                       initializer=self.initializer,
                                       trainable=True)
        self.betas = self.add_weight(name='betas',
                                     shape=(self.output_dim,),
                                     initializer=Constant(value=self.init_betas),
                                     # initializer='ones',
                                     trainable=True)

        super(RBFLayer, self).build(input_shape)

    def call(self, x):
        C = K.expand_dims(self.centers)
        H = K.transpose(C-K.transpose(x))
        return K.exp(-self.betas * K.sum(H**2, axis=1))

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)

    def get_config(self):
        config = {
            'output_dim': self.output_dim
        }
        base_config = super(RBFLayer, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class RBN(tf.keras.Model):

    def __init__(self,
                 initializer = None,
                 output_func:   str = None):
        super().__init__()

        self.rbf = RBFLayer(32, initializer)
        self.lin1 = tf.keras.layers.Dense(32, activation="relu")
        #self.lin2 = tf.keras.layers.Dense(32, activation="relu")
        self.output_layer = tf.keras.layers.Dense(1, activation=output_func)


    def call(self, inputs):
        prev_layer = tf.expand_dims(inputs, axis=-1)
        prev_layer = self.rbf(prev_layer)
        prev_layer = self.lin1(prev_layer)
        #prev_layer = self.lin2(prev_layer)

        return self.output_layer(prev_layer)

