def _init_for_train(self, keys: list[int], data: list[any]):
    sort_indexes = np.argsort(keys)

    self.N = len(keys)
    self.keys = np.array(keys)[sort_indexes]
    self.norm_keys = self._normalize(self.keys)
    self.data = np.array(data)[sort_indexes]
    self.positions = np.arange(0, self.N) / (self.N - 1)

def _true_train(self):
    self.model.fit(
            self.norm_keys,
            self.positions,
            batch_size=1,
            callbacks=[LossDiffStop(1e-3), self.metrics],
            epochs=30)

def train(self, keys: list[int], data: list[any]):
    self._init_for_train(keys, data)
    self.metrics = MetricCallback(self.norm_keys, self.positions)
    self._true_train()

    self.mean_abs_err = self.metrics.mean_abs_err
    self.max_abs_err = self.metrics.max_abs_err
    self.trained = True
