from indexes.builder import LindexBuilder

class TestLindex:
    index = LindexBuilder("fcnn2").build()

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

    def test_insert(self):
        assert self.index.N == 10

        self.index.insert(-100, 11)
        assert self.index.N == 11

        value =  self.index.find([-100])[0]
        assert value == 11
