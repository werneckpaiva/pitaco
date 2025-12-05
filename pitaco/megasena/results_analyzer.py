

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

@dataclass
class MegasenaResult:
    n: int
    dt: str
    numbers: List[int]

    def __post_init__(self):
        self.numbers = [int(n) for n in self.numbers]


class MegasenaResultsAnalyzer:

    results: List[MegasenaResult] = []

    def __init__(self):
        self.results = []

    def add_result(self, n: int, dt: str, numbers: List[int]) -> None:
        """Adds a new result to the analyzer."""
        result = MegasenaResult(
                n=n,
                dt=dt,
                numbers=numbers
        )
        self.results.append(result)
    
    def get_most_frequent(self, qnt: int = 0) -> List[Tuple[int, int]]:
        """Returns the most frequent numbers drawn."""
        freq: Dict[int, int] = {}
        for r in self.results:
            for n in r.numbers:
                freq[n] = freq.get(n, 0) + 1
        sorted_freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
        if qnt > 0: return sorted_freq[0:qnt]
        return sorted_freq

    
    def get_longest_numbers_missing(self, qnt: int = 0) -> List[Tuple[int, int]]:
        """Returns the numbers that haven't been drawn for the longest time."""
        numbers: Dict[int, int] = {}
        for i, r in enumerate(self.results[::-1]):
            for n in r.numbers:
                if n not in numbers:
                    numbers[n] = i
            if len(numbers) == 60:
                break
        sorted_numbers = sorted(numbers.items(), key=lambda x: x[1], reverse=True)
        if qnt > 0: return sorted_numbers[0:qnt]
        return sorted_numbers

    def count_odd_even(self) -> Dict[str, List[Tuple[int, int]]]:
        """Counts the occurrences of odd and even numbers in each draw."""
        odds: Dict[int, int] = {}
        evens: Dict[int, int] = {}
        for r in self.results:
            odd = sum(1 for i in r.numbers if i % 2 != 0)
            even = sum(1 for i in r.numbers if i % 2 == 0)
            
            if odd > 0:
                odds[odd] = odds.get(odd, 0) + 1
            if even > 0:
                evens[even] = evens.get(even, 0) + 1
        
        result = {
            "odd": sorted(odds.items(), reverse=True), 
            "even": sorted(evens.items(), reverse=True)
        }
        return result
    
    def count_adjacents_by(self, distance: int) -> Dict[int, int]:
        """Counts how many times numbers with a specific distance appear in the same draw."""
        frequency: Dict[int, int] = {}
        for r in self.results:
            numbers = sorted(r.numbers)
            count = 0
            for i in range(len(numbers) - 1):
                 # Check if any subsequent number is at 'distance'
                if numbers[i] + distance in numbers[i+1:]:
                    count += 1
            if count > 0:
                frequency[r.n] = count
        return frequency

    def get_total(self) -> int:
        """Returns the total number of results."""
        return len(self.results)

    def calculate_prob_odd_even(self, numbers: List[int]) -> Tuple[float, float]:
        """Calculates the probability of odd and even numbers based on historical data."""
        n_evens = sum([1 for n in numbers if n%2==0])
        qnt_numbers = len(numbers)
        total_evens = 0.0
        for r in self.results:
            total_partial = len(r.numbers) - qnt_numbers
            if total_partial == 0: continue # Avoid division by zero if full draw matches input length
            
            r_evens = sum([1 for n in r.numbers if n%2==0])
            qnt_evens = r_evens - n_evens
            p_even = qnt_evens / float(total_partial) if qnt_evens >= 0 else 0
            total_evens += p_even
        
        if not self.results:
            return 0.0, 0.0

        total_p_even = total_evens / len(self.results)
        return (1-total_p_even), total_p_even
