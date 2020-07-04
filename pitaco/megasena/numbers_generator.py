from random import uniform
from pitaco.megasena.file_loader import MegasenaFileLoader


class MegasenaNumberGenerator(object):

    numbers = None
    result_analyzer = None
    
    def __init__(self, folder):
        loader = MegasenaFileLoader(folder)
        self.result_analyzer = loader.load_from_csv()

    def calc_frequency(self):
        freq = self.result_analyzer.get_most_frequent()
        highest = float(freq[0][1])
        lowest = float(freq[-1][1])
        delta = float(highest - lowest)
        for (n, f) in freq:
            p = self.numbers[n-1][1]
            new_p = (((f - lowest) / delta) * 4)
            self.numbers[n-1] = (n, p + new_p)

    def calc_missing_numbers(self):
        missing = self.result_analyzer.get_longest_numbers_missing()
        highest = float(missing[0][1])
        lowest = float(missing[-1][1])
        delta = float(highest - lowest)
        for (n, f) in missing:
            p = self.numbers[n-1][1]
            new_p = (((f - lowest) / delta) * 4)
            self.numbers[n-1] = (n, p + new_p)

    def sample(self):
        total = sum([p for n, p in self.numbers])
        r = int(uniform(0, total) * 100) / 100.0
        p_count = 0
        for i, (n, p) in enumerate(self.numbers):
            p_count += p
            if p_count >= r:
                self.numbers.pop(i)
                break
        return n

    def calculate_odds_evens(self, numbers):
        if len(numbers) == 6:
            return
        (p_odd, p_even) = self.result_analyzer.calculate_prob_odd_even(numbers)
        for i, (n, p) in enumerate(self.numbers):
            new_p = (p_odd if n % 2 == 1 else p_even) * 2
            self.numbers[i] = (n, p + new_p)

    def generate(self):
        self.numbers = list(zip(range(1, 61), [1]*60))
        self.calc_frequency()
        self.calc_missing_numbers()

        numbers = []
        for _ in range(6):
            numbers.append(self.sample())
            self.calculate_odds_evens(numbers)
        numbers = sorted(numbers)
        return numbers

    def _generate(self):
        r = [0] * 60  
        for _ in range(5000):
            numbers = self._generate()
            for n in numbers:
                r[n-1] += 1
        print("Sorteados: ")
        print(sorted([(i+1, n) for (i, n) in enumerate(r)], key=lambda x: x[1], reverse=True))
        return self._generate()
