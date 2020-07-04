

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
    
    def get_most_frequent(self, qnt=0):
        freq = {}
        for r in self.results:
            for n in r.numbers:
                freq[n] = freq.get(n, 0) + 1
        sorted_freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
        if qnt > 0: sorted_freq[0:qnt]
        return sorted_freq

    
    def get_longest_numbers_missing(self, qnt=0):
        numbers = {}
        for i, r in enumerate(self.results[::-1]):
            for n in r.numbers:
                if n not in numbers:
                    numbers[n] = i
            if len(numbers) == 60:
                break
        sorted_numbers = sorted(numbers.items(), key=lambda x: x[1], reverse=True)
        if qnt > 0: sorted_numbers[0:qnt]
        return sorted_numbers

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
            for i in range(5):
                if numbers[i] + distance in numbers[i+1:]:
                    count += 1
            if count > 0:
                frequency[r.n] = count
        return frequency

    def get_total(self):
        return len(self.results)

    def calculate_prob_odd_even(self, numbers):
        n_evens = sum([1 for n in numbers if n%2==0])
        qnt_numbers = len(numbers)
        total_evens = 0
        for r in self.results:
            total_partial = len(r.numbers) - qnt_numbers
            r_evens = sum([1 for n in r.numbers if n%2==0])
            qnt_evens = r_evens - n_evens
            p_even = qnt_evens / float(total_partial) if qnt_evens >= 0 else 0
            total_evens += p_even
        total_p_even = total_evens / len(self.results)
        return (1-total_p_even), total_p_even
