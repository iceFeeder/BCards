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
            self._swap(count, random.randint(0, length-1))
            count += 1
        return self.pool

    def get_pool(self):
        return self.pool

    @abc.abstractmethod
    def get_cards(self, index=0):
        raise NotImplementedError

    @abc.abstractmethod
    def check(self, play_cards, player_id):
        raise NotImplementedError

    def reset(self):
        self.shuffle()

    @abc.abstractmethod
    def clear(self):
        raise NotImplementedError
