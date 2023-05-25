def _clarify(self, keys, positions):
    def clarify_one(key, position):
        position = max(min(position, self.N - 1), 0)

        low = max(position - self.mean_abs_err, 0)
        high = min(position + self.mean_abs_err, self.N - 1)

        if not (self.keys[low] < key < self.keys[high]):
            low = max(position - self.max_abs_err, 0)
            high = min(position + self.max_abs_err, self.N - 1)

        return binsearch(self.keys, low, high, key)

    vec_clarify = np.vectorize(clarify_one)
    positions = vec_clarify(keys, positions)
    return positions[positions >= 0]
