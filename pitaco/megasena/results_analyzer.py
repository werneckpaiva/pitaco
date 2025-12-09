

from dataclasses import dataclass
from typing import List, Dict, Tuple
from functools import lru_cache as cache

@dataclass
class MegasenaResult:
    n: int
    dt: str
    numbers: List[int]

    def __post_init__(self):
        self.numbers = [int(n) for n in self.numbers]


@dataclass
class GapAnalysisResult:
    sorted_distributions: List[Dict[int, float]]
    repetition_stats: Dict[str, float]
    common_repeated_gaps: Dict[int, float]


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
    
    @cache
    def get_most_frequent(self, qnt: int = 0) -> List[Tuple[int, int]]:
        """Returns the most frequent numbers drawn."""
        freq: Dict[int, int] = {}
        for r in self.results:
            for n in r.numbers:
                freq[n] = freq.get(n, 0) + 1
        sorted_freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
        if qnt > 0: return sorted_freq[0:qnt]
        return sorted_freq

    @cache
    def get_numbers_by_absence_duration(self, qnt: int = 0) -> List[Tuple[int, int]]:
        """Returns the numbers that haven't been drawn for the longest time, sorted by their absence duration."""
        numbers: Dict[int, int] = {}
        for i, r in enumerate(self.results[::-1]):
            for n in r.numbers:
                if n not in numbers:
                    numbers[n] = i
            if len(numbers) == 60:  # Assuming 60 possible numbers in Megasena (1-60)
                break
        sorted_numbers = sorted(numbers.items(), key=lambda x: x[1], reverse=True)
        if qnt > 0: return sorted_numbers[0:qnt]
        return sorted_numbers

    @cache
    def get_sorted_gap_distributions(self) -> GapAnalysisResult:
        """
        Calculates the probability distributions for each sorted gap position and repetition statistics.
        Returns a GapAnalysisResult containing:
        - sorted_distributions: List of 5 dicts, probability of gap values at each sorted position.
        - repetition_stats: Probability of having 'unique' gaps, 'one_pair', or 'multiple_repetitions'.
        - common_repeated_gaps: Probability of specific gap values being the repeated one (when one pair exists).
        """
        gap_position_counts: List[Dict[int, int]] = [{} for _ in range(5)]
        repetition_counts: Dict[str, int] = {"unique": 0, "one_pair": 0, "multiple_repetitions": 0}
        repeated_value_counts: Dict[int, int] = {}
        
        total_draws = 0

        for r in self.results:
            numbers = sorted(r.numbers)
            if len(numbers) < 6: continue
            
            # Calculate gaps
            gaps = [numbers[i+1] - numbers[i] for i in range(len(numbers) - 1)]
            # Sort gaps (smallest to largest)
            sorted_gaps = sorted(gaps)
            
            if len(sorted_gaps) == 5:
                # 1. Sorted Position Stats
                for i in range(5):
                    gap_val = sorted_gaps[i]
                    gap_position_counts[i][gap_val] = gap_position_counts[i].get(gap_val, 0) + 1
                
                # 2. Repetition Stats
                unique_gaps = set(sorted_gaps)
                if len(unique_gaps) == 5:
                    repetition_counts["unique"] += 1
                elif len(unique_gaps) == 4:
                    repetition_counts["one_pair"] += 1
                    # Find the repeated value
                    for g in unique_gaps:
                        if sorted_gaps.count(g) == 2:
                            repeated_value_counts[g] = repeated_value_counts.get(g, 0) + 1
                            break
                else:
                    repetition_counts["multiple_repetitions"] += 1

                total_draws += 1
        
        if total_draws == 0:
            return self.GapAnalysisResult([{} for _ in range(5)], {}, {})

        # Normalize
        sorted_distributions = []
        for counts in gap_position_counts:
            dist = {gap: count / total_draws for gap, count in counts.items()}
            sorted_distributions.append(dist)
        
        repetition_stats = {k: v / total_draws for k, v in repetition_counts.items()}
        
        total_one_pairs = repetition_counts["one_pair"]
        common_repeated_gaps = {}
        if total_one_pairs > 0:
             common_repeated_gaps = {k: v / total_one_pairs for k, v in repeated_value_counts.items()}

        return GapAnalysisResult(
            sorted_distributions=sorted_distributions,
            repetition_stats=repetition_stats,
            common_repeated_gaps=common_repeated_gaps
        )
