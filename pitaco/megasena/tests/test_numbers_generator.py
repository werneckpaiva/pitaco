import unittest
from unittest.mock import MagicMock, patch
from pitaco.megasena.numbers_generator import MegasenaNumberGenerator


class NumbersGeneratorTest(unittest.TestCase):

    @patch('pitaco.megasena.numbers_generator.MegasenaFileLoader')
    def test_generate_6_numbers(self, MockFileLoader):
        # Setup mock
        mock_loader_instance = MockFileLoader.return_value
        mock_analyzer = MagicMock()
        mock_loader_instance.load_from_csv.return_value = mock_analyzer
        
        # Setup analyzer mocks to return dummy data needed for generate()
        mock_analyzer.get_most_frequent.return_value = [(1, 10), (2, 5)] # Example data
        mock_analyzer.get_numbers_by_absence_duration.return_value = [(3, 10), (4, 5)] # Example data
        # Return 5 dicts for 5 gaps
        mock_gap_result = MagicMock()
        mock_gap_result.sorted_distributions = [{1: 1.0}, {2: 1.0}, {3: 1.0}, {4: 1.0}, {5: 1.0}]
        mock_gap_result.repetition_stats = {"unique": 1.0, "one_pair": 0.0, "multiple_repetitions": 0.0}
        mock_analyzer.get_sorted_gap_distributions.return_value = mock_gap_result

        generator = MegasenaNumberGenerator("dummy_folder")
        numbers = generator.generate()
        self.assertEqual(6, len(numbers))


if __name__ == "__main__":
    unittest.main()