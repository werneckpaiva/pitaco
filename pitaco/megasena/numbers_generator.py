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

    result_analyzer: MegasenaResultsAnalyzer
    
    def __init__(self, folder: str):
        loader = MegasenaFileLoader(folder)
        self.result_analyzer = loader.load_from_csv()

    def _update_weights_based_on_frequency(self, numbers: List[Tuple[int, float]]) -> List[Tuple[int, float]]:
        """
        Adjusts the probability weights of numbers based on their historical frequency.
        Returns a new list with updated weights.
        """
        new_numbers = list(numbers)

        freq_list = self.result_analyzer.get_most_frequent()
        if not freq_list:
            return new_numbers

        highest = float(freq_list[0][1])
        lowest = float(freq_list[-1][1])
        delta = highest - lowest
        
        if delta == 0:
            return new_numbers

        
        for (n, f) in freq_list:
            # numbers is 0-indexed list of tuples (number, weight)
            # n from analyzer is 1-based number (1 to 60)
            idx = n - 1
            current_n, current_weight = new_numbers[idx]
            
            # Normalize frequency contribution
            weight_adjustment = (((f - lowest) / delta) * 4)
            new_numbers[idx] = (current_n, current_weight + weight_adjustment)
        return new_numbers

    def _update_weights_based_on_missing(self, numbers: List[Tuple[int, float]]) -> List[Tuple[int, float]]:
        """
        Adjusts weights based on how long numbers have been missing.
        Returns a new list with updated weights.
        """

        new_numbers = list(numbers)

        missing_list = self.result_analyzer.get_numbers_by_absence_duration()
        if not missing_list:
            return new_numbers

        highest = float(missing_list[0][1])
        lowest = float(missing_list[-1][1])
        delta = highest - lowest

        if delta == 0:
            return new_numbers

        for (n, f) in missing_list:
            idx = n - 1
            current_n, current_weight = new_numbers[idx]
            
            weight_adjustment = (((f - lowest) / delta) * 4)
            new_numbers[idx] = (current_n, current_weight + weight_adjustment)
        return new_numbers

    def _sample_number(self, numbers: List[Tuple[int, float]]) -> int:
        """
        Samples one number from the available numbers based on weights.
        Removes the chosen number from self.numbers to avoid duplicates in a single draw.
        """
        total_weight = sum(weight for _, weight in numbers)
        r = uniform(0, total_weight)
        
        cumulative_weight = 0.0
        for i, (n, weight) in enumerate(numbers):
            cumulative_weight += weight
            if cumulative_weight >= r:
                numbers.pop(i)
                return n
        
        # Fallback in case of rounding errors, return last one
        return numbers.pop()[0]

    def _generate_candidate(self, numbers: List[Tuple[int, float]]) -> List[int]:
        """
        Generates a single candidate draw using the given weights.
        """
        # Clone numbers list because _sample_number pops items
        current_numbers = list(numbers)
        result_numbers: List[int] = []
        for _ in range(6):
            if not current_numbers: break
            selected_number = self._sample_number(current_numbers)
            result_numbers.append(selected_number)
        return sorted(result_numbers)

    def generate(self, num_candidates: int = 1000, use_frequency: bool = True, use_missing: bool = True, use_gaps: bool = True) -> List[int]:
        """
        Generates a sequence of 6 unique numbers.
        
        Args:
            num_candidates: Number of candidates to generate/consider.
            use_frequency: If True, adjusts weights based on historical frequency.
            use_missing: If True, adjusts weights based on how long numbers have been missing.
            use_gaps: If True, enforces historical gap distributions and repetition patterns.
        """
        # 1. Calculate Number Weights
        # Initialize numbers 1..60 with a base weight of 1.0
        # Format: list of [number, weight] to allow modification
        weighted_numbers = [[i, 1.0] for i in range(1, 61)]
        
        # We need to pass list of tuples to helper methods, but they modify it in place? 
        # The helpers expect List[Tuple[int, float]] but try to assign to it? 
        # Actually existing helpers:
        # def _update_weights_based_on_frequency(self, numbers: List[Tuple[int, float]]) -> None:
        #     ...
        #     numbers[idx] = (current_n, current_weight + weight_adjustment)
        # So they expect a list that can be mutated. A list of tuples is fine if we replace the tuple.

        # Let's convert to list of tuples for compatibility with existing helpers
        weighted_numbers_tuples = [(i, 1.0) for i in range(1, 61)]

        if use_frequency:
            weighted_numbers_tuples = self._update_weights_based_on_frequency(weighted_numbers_tuples)
        
        if use_missing:
            weighted_numbers_tuples = self._update_weights_based_on_missing(weighted_numbers_tuples)

        # 2. Generate Numbers
        if use_gaps:
             return self._generate_with_gaps_and_weights(num_candidates, weighted_numbers_tuples, use_scoring=use_frequency or use_missing)
        else:
             return self._generate_with_weights_only(weighted_numbers_tuples)

    def _generate_with_weights_only(self, weighted_numbers: List[Tuple[int, float]]) -> List[int]:
        """Generates a single draw using only the provided weights."""
        return self._generate_candidate(weighted_numbers)

    def _generate_with_gaps_and_weights(self, num_candidates: int, weighted_numbers: List[Tuple[int, float]], use_scoring: bool) -> List[int]:
        """
        Generates candidates using gap logic. 
        If use_scoring is True, picks the best candidate based on weights.
        Otherwise returns the first valid candidate.
        """
        from random import choices, shuffle, randint

        # Create a lookup for weights for fast scoring
        weight_map = {n: w for n, w in weighted_numbers}

        stats = self.result_analyzer.get_sorted_gap_distributions()
        sorted_dists = stats.sorted_distributions
        repetition_stats = stats.repetition_stats

        # Prepare value/weight lists for efficient sampling
        dist_choices = []
        for d in sorted_dists:
            vals = list(d.keys())
            weights = list(d.values())
            dist_choices.append((vals, weights))
        
        rep_modes = list(repetition_stats.keys())
        rep_weights = list(repetition_stats.values())

        best_draw = []
        best_score = -1.0

        for _ in range(num_candidates):
            # 1. Determine Target Repetition Mode
            mode = choices(rep_modes, rep_weights)[0]

            # 2. Sample 5 gap values from sorted positions
            cand_gaps = []
            
            # Sample each position
            for i in range(5):
                vals, weights = dist_choices[i]
                g = choices(vals, weights)[0]
                cand_gaps.append(g)
            
            # Check 1: Must be effectively sorted
            if sorted(cand_gaps) != cand_gaps:
                continue

            # Check 2: Repetition Constraints
            counts = {x: cand_gaps.count(x) for x in cand_gaps}
            unique_count = len(counts)
            
            if mode == "unique":
                if unique_count != 5: continue
            elif mode == "one_pair":
                if unique_count != 4: continue
            elif mode == "multiple_repetitions":
                if unique_count > 3: continue
            
            # 3. Construct Draw
            permuted_gaps = list(cand_gaps)
            shuffle(permuted_gaps)
            
            current_sum = sum(permuted_gaps)
            max_start = 60 - current_sum
            
            if max_start < 1:
                continue
            
            # Pick a start number
            start_num = randint(1, max_start)
            
            draw = [start_num]
            curr = start_num
            for g in permuted_gaps:
                curr += g
                draw.append(curr)
            
            candidate = sorted(draw)
            
            if not use_scoring:
                # If no weights involvement, just return the first valid one
                return candidate
            
            # Score the candidate
            # Score = sum of weights? or product. 
            # Original logic was product for probabilities. 
            # Weights are somewhat arbitrary (frequency based). 
            # Let's use Sum of weights as a simple fitness metric for now, 
            # or Product if weights are treated as probabilities.
            # Since _update_weights adds small increments, let's use Sum.
            score = sum(weight_map[n] for n in candidate)
            
            if score > best_score:
                best_score = score
                best_draw = candidate
        
        return best_draw if best_draw else []

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
