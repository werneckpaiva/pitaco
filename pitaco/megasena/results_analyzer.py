

class MegasenaResult():

    n = None
    dt = None
    numbers = None

    def __init__(self, n, dt, numbers):
        self.n = n
        self.dt = dt
        self.numbers = [int(n) for n in numbers]


class MegasenaResultsAnalyzer:

    results = []

    def __init__(self):
        self.results = []

    def add_result(self, n, dt, numbers):
        result = MegasenaResult(
                n=n,
                dt=dt,
                numbers=numbers
        )
        self.results.append(result)
    
    def get_most_frequent(self, qnt):
        freq = {}
        for r in self.results:
            for n in r.numbers:
                freq[n] = freq.get(n, 0) + 1
        sorted_freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
        return sorted_freq[0:qnt]

    
    def get_longest_numbers_missing(self, qnt):
        numbers = {}
        for i, r in enumerate(self.results[::-1]):
            for n in r.numbers:
                if n not in numbers:
                    numbers[n] = i
            if len(numbers) == 60:
                break
        sorted_numbers = sorted(numbers.items(), key=lambda x: x[1], reverse=True)
        return sorted_numbers[0:qnt]

    def count_odd_even(self):
        odds = {}
        evens = {}
        for r in self.results:
            odd = 0
            even = 0
            for i in r.numbers:
                if i % 2 == 0:
                    even += 1
                else:
                    odd += 1
            if odd > 0:
                odds[odd] = odds.get(odd, 0) + 1
            if even > 0:
                evens[even] = evens.get(even, 0) + 1
        result = {"odd":sorted(odds.items(), reverse=True), 
                  "even":sorted(evens.items(), reverse=True)}
        return result

    
    def count_adjacents_by(self, distance):
        frequency = {}
        for r in self.results:
            numbers = sorted(r.numbers)
            count = 0
            for i in xrange(5):
                if numbers[i] + distance in numbers[i+1:]:
                    count += 1
            if count > 0:
                frequency[r.n] = count
        return frequency
