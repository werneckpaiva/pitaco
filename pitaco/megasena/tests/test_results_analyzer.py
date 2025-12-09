from pitaco.megasena.numbers_generator import MegasenaNumberGenerator
import unittest
from pitaco.megasena.results_analyzer import MegasenaResultsAnalyzer
from datetime import date
from os.path import dirname, join

class ResultsAnalyzerTest(unittest.TestCase):

    def test_add_results(self):
        analyzer = MegasenaResultsAnalyzer()
        analyzer.add_result(1, date.today(), [1,2,3,4,5,6])
        analyzer.add_result(2, date.today(), [7, 8, 9, 10, 11, 12])

        self.assertEqual(len(analyzer.results), 2)

    def test_3_most_frequent_numbers(self):
        analyzer = MegasenaResultsAnalyzer()
        analyzer.add_result(1, date.today(), [1, 2, 3, 4, 5, 6])
        analyzer.add_result(2, date.today(), [1, 2, 3, 10, 11, 12])
        analyzer.add_result(3, date.today(), [1, 2, 15, 16, 17, 18])
        
        frequent_numbers = analyzer.get_most_frequent(3)
        self.assertEqual(frequent_numbers, [(1,3), (2,3), (3,2)])

    def test_longest_numbers_missing(self):
        analyzer = MegasenaResultsAnalyzer()
        analyzer.add_result(1, date.today(), [1, 2, 3, 4, 5, 6])
        analyzer.add_result(2, date.today(), [2, 3, 4, 5, 6, 7])
        analyzer.add_result(3, date.today(), [3, 4, 5, 6, 7, 8])
        analyzer.add_result(4, date.today(), [3, 18, 5, 6, 7, 8])

        numbers = analyzer.get_numbers_by_absence_duration(3)
        self.assertEqual(numbers, [(1, 3), (2, 2), (4, 1)])





    def test_get_sorted_gap_distributions(self):
        analyzer = MegasenaResultsAnalyzer()
        # R1: [1, 2, 4, 7, 11, 16] 
        # Gaps: 1, 2, 3, 4, 5. Sorted: 1, 2, 3, 4, 5
        analyzer.add_result(1, date.today(), [1, 2, 4, 7, 11, 16])
        
        # R2: [10, 20, 30, 40, 50, 60]
        # Gaps: 10, 10, 10, 10, 10. Sorted: 10, 10, 10, 10, 10
        analyzer.add_result(2, date.today(), [10, 20, 30, 40, 50, 60])
        
        result = analyzer.get_sorted_gap_distributions()
        dists = result.sorted_distributions
        self.assertEqual(len(dists), 5)
        # Position 0 (smallest gap):
        # R1 has 1. R2 has 10.
        # Prob: {1: 0.5, 10: 0.5}
        self.assertEqual(dists[0], {1: 0.5, 10: 0.5})
        
        # Position 4 (largest gap):
        # R1 has 5. R2 has 10.
        # Prob: {5: 0.5, 10: 0.5}
        self.assertEqual(dists[4], {5: 0.5, 10: 0.5})
    


        
