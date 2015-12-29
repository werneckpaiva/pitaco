from random import sample


class MegasenaNumberGenerator(object):

    numbers = set(range(1, 61))

    def generate(self):
        numbers = sample(self.numbers, 6)
        numbers = sorted(numbers)
        return numbers
