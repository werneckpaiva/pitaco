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
        mock_analyzer.get_longest_numbers_missing.return_value = [(3, 10), (4, 5)] # Example data
        mock_analyzer.calculate_prob_odd_even.return_value = (0.5, 0.5)

        generator = MegasenaNumberGenerator("dummy_folder")
        numbers = generator.generate()
        self.assertEqual(6, len(numbers))


if __name__ == "__main__":
    unittest.main()