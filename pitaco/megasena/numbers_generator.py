from random import uniform
from typing import List, Tuple, Optional
import logging
from pitaco.megasena.file_loader import MegasenaFileLoader
from pitaco.megasena.results_analyzer import MegasenaResultsAnalyzer

LOG = logging.getLogger(__name__)


class MegasenaNumberGenerator:
    """
    Generates Mega Sena numbers based on historical frequency and missing number patterns.
    """

    numbers: List[Tuple[int, float]]
    result_analyzer: MegasenaResultsAnalyzer
    
    def __init__(self, folder: str):
        loader = MegasenaFileLoader(folder)
        self.result_analyzer = loader.load_from_csv()
        self.numbers = []

    def _update_weights_based_on_frequency(self) -> None:
        """
        Adjusts the probability weights of numbers based on their historical frequency.
        Less frequent numbers get a higher weight adjustment? 
        (Original logic: new_p = (((f - lowest) / delta) * 4))
        Wait, looking at original logic:
        freq = most frequent numbers.
        highest = max frequency.
        lowest = min frequency.
        (f - lowest) / delta -> normalizes frequency 0..1
        Then * 4.
        So higher frequency -> higher weight adjustment.
        """
        freq_list = self.result_analyzer.get_most_frequent()
        if not freq_list:
            return

        highest = float(freq_list[0][1])
        lowest = float(freq_list[-1][1])
        delta = highest - lowest
        
        if delta == 0:
            return

        for (n, f) in freq_list:
            # numbers is 0-indexed list of tuples (number, weight)
            # n from analyzer is 1-based number (1 to 60)
            idx = n - 1
            current_n, current_weight = self.numbers[idx]
            
            # Normalize frequency contribution
            weight_adjustment = (((f - lowest) / delta) * 4)
            self.numbers[idx] = (current_n, current_weight + weight_adjustment)

    def _update_weights_based_on_missing(self) -> None:
        """
        Adjusts weights based on how long numbers have been missing.
        """
        missing_list = self.result_analyzer.get_longest_numbers_missing()
        if not missing_list:
            return

        highest = float(missing_list[0][1])
        lowest = float(missing_list[-1][1])
        delta = highest - lowest

        if delta == 0:
            return

        for (n, f) in missing_list:
            idx = n - 1
            current_n, current_weight = self.numbers[idx]
            
            weight_adjustment = (((f - lowest) / delta) * 4)
            self.numbers[idx] = (current_n, current_weight + weight_adjustment)

    def _sample_number(self) -> int:
        """
        Samples one number from the available numbers based on weights.
        Removes the chosen number from self.numbers to avoid duplicates in a single draw.
        """
        total_weight = sum(weight for _, weight in self.numbers)
        r = uniform(0, total_weight)
        
        cumulative_weight = 0.0
        for i, (n, weight) in enumerate(self.numbers):
            cumulative_weight += weight
            if cumulative_weight >= r:
                self.numbers.pop(i)
                return n
        
        # Fallback in case of rounding errors, return last one
        return self.numbers.pop()[0]

    def _adjust_weights_for_parity(self, current_selection: List[int]) -> None:
        """
        Adjusts weights of remaining numbers to balance odd/even distribution.
        """
        if len(current_selection) == 6:
            return
            
        p_odd, p_even = self.result_analyzer.calculate_prob_odd_even(current_selection)
        
        for i, (n, weight) in enumerate(self.numbers):
            # n is the number. If n is odd, boost by p_odd, else p_even.
            # Original logic: new_p = (p_odd if n % 2 == 1 else p_even) * 2
            weight_boost = (p_odd if n % 2 == 1 else p_even) * 2
            self.numbers[i] = (n, weight + weight_boost)

    def generate(self) -> List[int]:
        """
        Generates a sequence of 6 unique numbers.
        """
        # Initialize numbers 1..60 with a base weight of 1
        self.numbers = list(zip(range(1, 61), [1.0] * 60))
        
        self._update_weights_based_on_frequency()
        self._update_weights_based_on_missing()

        result_numbers: List[int] = []
        for _ in range(6):
            selected_number = self._sample_number()
            result_numbers.append(selected_number)
            self._adjust_weights_for_parity(result_numbers)
            
        return sorted(result_numbers)

    def simulate(self, iterations: int = 5000) -> List[Tuple[int, int]]:
        """
        Runs a simulation of draws to see the distribution of generated numbers.
        """
        counts = [0] * 60  
        for _ in range(iterations):
            numbers = self.generate()
            for n in numbers:
                counts[n-1] += 1
        
        # Sort by frequency desc
        result = sorted([(i+1, count) for (i, count) in enumerate(counts)], key=lambda x: x[1], reverse=True)
        
        LOG.info("Simulation Results (Number, Frequency):")
        LOG.info(result)
        return result
