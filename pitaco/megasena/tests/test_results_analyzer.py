import unittest
from pitaco.megasena.results_analyzer import MegasenaResultsAnalyzer
from datetime import date


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

        numbers = analyzer.get_longest_numbers_missing(3)
        self.assertEqual(numbers, [(1, 3), (2, 2), (4, 1)])

    def test_count_odd_even_frequency_only_evens(self):
        analyzer = MegasenaResultsAnalyzer()
        analyzer.add_result(1, date.today(), [2, 4, 6, 8, 10, 12])
        analyzer.add_result(2, date.today(), [2, 4, 6, 8, 10, 12])
        result = analyzer.count_odd_even()
        self.assertEqual(result, {"even":[(6, 2)], "odd":[]})

    def test_count_odd_even_frequency(self):
        analyzer = MegasenaResultsAnalyzer()
        analyzer.add_result(1, date.today(), [1, 2, 3, 4, 5, 6])
        analyzer.add_result(2, date.today(), [7, 8, 9, 10, 11, 12])
        analyzer.add_result(3, date.today(), [1, 3, 5, 7, 9, 11])
        result = analyzer.count_odd_even()
        self.assertEqual(result, {"even":[(3, 2)], "odd":[(6, 1), (3, 2)]})

    def test_count_adjacents_by_1(self):
        analyzer = MegasenaResultsAnalyzer()
        analyzer.add_result(1, date.today(), [1, 2, 4, 9, 11, 14])
        analyzer.add_result(2, date.today(), [3, 4, 5, 12, 16, 30])
        
        result = analyzer.count_adjacents_by(1)
        self.assertEqual(result, {1: 1, 2:2})

    def test_count_adjacents_by_2(self):
        analyzer = MegasenaResultsAnalyzer()
        analyzer.add_result(1, date.today(), [1, 2, 4, 9, 11, 14])
        analyzer.add_result(2, date.today(), [3, 4, 5, 12, 16, 30])
        
        result = analyzer.count_adjacents_by(2)
        self.assertEqual(result, {1: 2, 2:1})