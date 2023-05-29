from indexes.builder import LindexBuilder

class TestLindex:
    index = LindexBuilder("fcnn2-pt").build()

    def test_train(self):
        keys = [7, -10, 4, 6, 38, -8, 3, -11, 1, 90]
        data = [10,  9, 8, 7,  6,  5, 4,   3, 2,  1]
        self.index.train(keys, data)

        assert self.index.trained

    def test_middle(self):
        value = self.index.find([3])[0]
        assert value == 4

    def test_first(self):
        value = self.index.find([-11])[0]
        assert value == 3

    def test_last(self):
        value = self.index.find([90])[0]
        assert value == 1

    def test_not_exist(self):
        value = self.index.find([5])[0]
        assert value.size == 0

    def test_range_lw_in(self):
        values, _ = self.index.predict_range((None, 4), (None, 1))
        assert set([3, 9, 5, 2, 4]) == set(values)

    def test_range_lw_out(self):
        values, _ = self.index.predict_range((None, 59), (None, 1))
        assert set([3, 9, 5, 2, 4, 8, 7, 10, 6]) == set(values)

    def test_range_gr_in(self):
        values, _ = self.index.predict_range((38, None), (1, None))
        assert set([1]) == set(values)

    def test_range_gr_out(self):
        values, _ = self.index.predict_range((0, None), (1, None))
        assert set([2, 4, 8, 7, 10, 6, 1]) == set(values)

    def test_range_le_in(self):
        values, _ = self.index.predict_range((None, 1), (None, 0))
        assert set([3, 9, 5, 2]) == set(values)

    def test_range_le_out(self):
        values, _ = self.index.predict_range((None, -9), (None, 0))
        assert set([3, 9]) == set(values)

    def test_range_ge_in(self):
        values, _ = self.index.predict_range((7, None), (0, None))
        assert set([10, 6, 1]) == set(values)

    def test_range_ge_out(self):
        values, _ = self.index.predict_range((5, None), (0, None))
        assert set([7, 10, 6, 1]) == set(values)

    def test_range_gle(self):
        values, _ = self.index.predict_range((-10, 6), (0, 0))
        assert set([9, 5, 2, 4, 8, 7]) == set(values)

    def test_range_gle_all(self):
        values, _ = self.index.predict_range((-100, 100), (0, 0))
        assert set([3, 9, 5, 2, 4, 8, 7, 10, 6, 1]) == set(values)

    def test_range_gle_none(self):
        values, _ = self.index.predict_range((40, 50), (0, 0))
        assert set([]) == set(values)

    def test_insert(self):
        assert self.index.N == 10

        self.index.insert(-100, 11)
        assert self.index.N == 11

        value =  self.index.find([-100])[0]
        assert value == 11

