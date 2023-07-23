def _predict(self, keys):
    if not self.trained:
        return None

    keys = self._normalize(keys)
    pposition = self.model(keys)
    return np.around(pposition * self.N).astype(int).reshape(-1)

def find(self, keys):
    if not self.trained or not keys:
        return None

    keys = np.array(keys)
    positions = self._predict(keys)
    positions = self._clarify(keys, positions)
    return self.data[positions]
