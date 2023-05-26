import tensorflow as tf

class FCNN(tf.keras.Model):

    def __init__(self,
                 hidden_layers: list[tuple[int, str, tf.keras.initializers.Initializer]],
                 output_func:   str = None):
        super().__init__()

        self.output_func = output_func
        self.hidden_layers_types = hidden_layers
        self.hidden_layers = []
        for neurons_num, activation, initializer in hidden_layers:
            self.hidden_layers.append(
                    tf.keras.layers.Dense(neurons_num,
                                          activation=activation,
                                          kernel_initializer=initializer,
                                          bias_initializer=initializer))

        self.output_layer = tf.keras.layers.Dense(1, activation=self.output_func)


    def call(self, inputs):
        prev_layer  = tf.expand_dims(inputs, axis=-1)

        for layer in self.hidden_layers:
            prev_layer = layer(prev_layer)

        return self.output_layer(prev_layer)


    def get_config(self):
        return {"hidden_layers": self.hidden_layers_types,
                "output_func"  : self.output_func}


    @classmethod
    def from_config(cls, config):
        print(config)
        return cls(**config)

