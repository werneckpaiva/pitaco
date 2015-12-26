from random import sample


class MegasenaNumberGenerator(object):

    numbers = set(range(1, 61))

    def generate(self):
        return sample(self.numbers, 6)
