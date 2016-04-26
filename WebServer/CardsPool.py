import random

colors = [(c+1)*100 for c in range(4)]
nums = [n for n in range(13)]

class CardsPool:
    def __init__(self):
        self.pool = []
        for c in colors:
            for n in nums:
                self.pool.append(c+n)

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
        print self.pool

