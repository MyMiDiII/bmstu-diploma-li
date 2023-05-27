from keras.callbacks import Callback
import numpy as np

class MetricsCallback(Callback):
    def __init__(self, x, y_true):
        super(MetricsCallback, self).__init__()
        self.x = x
        self.y_true = y_true
        self.N = len(x)
        self.max_absolute_error = 0
        self.mean_absolute_error = 0

    def on_train_end(self, logs=None):
        y_pred = self.model.predict(self.x, verbose=0).reshape(-1)
        print("pred", y_pred)
        print("true", self.y_true)
        true_ae = np.abs(self.y_true - y_pred)
        print("tae", true_ae)
        absolute_errors = np.abs(np.round(self.y_true * self.N)
                           - np.round(y_pred * self.N)).astype(int)
        print("mae1", absolute_errors, np.mean(absolute_errors))
        absolute_errors = np.round(np.abs(self.y_true - y_pred) * self.N).astype(int)
        print("mae2", absolute_errors, np.mean(absolute_errors))

        self.max_absolute_error = np.max(absolute_errors)
        self.mean_absolute_error = np.ceil(np.mean(absolute_errors)).astype(int)

        self.mean_true_ae = np.mean(true_ae)
        print(f"Max Absolute Error: {self.max_absolute_error:.4f}")
        print(f"Mean Absolute Error: {self.mean_absolute_error:.4f}")
        print(f"True MEA: {self.mean_true_ae:.4f}")
