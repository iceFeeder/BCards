import random
import abc


class CardsPool(object):
    def __init__(self, size):
        self.pool = []
        for i in range(size):
            self.pool.append(i)

    def _swap(self, i, j):
        tmp = self.pool[i]
        self.pool[i] = self.pool[j]
        self.pool[j] = tmp

    def shuffle(self):
        count = 0
        length = len(self.pool)
        while count < length:
            self._swap(count, int(random.random() * (count+1)))
            count += 1
        return self.pool

    def get_pool(self):
        return self.pool

    def get_cards(self, index=0):
        return self.pool[int(index)::4]

    def check(self, data):
        return self.check_cards(data)

    @abc.abstractmethod
    def check_cards(self, data):
        raise NotImplementedError
