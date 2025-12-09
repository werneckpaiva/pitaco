import unittest
from unittest.mock import MagicMock, patch
from pitaco.megasena.numbers_generator import MegasenaNumberGenerator
from pitaco.megasena.results_analyzer import MegasenaResultsAnalyzer

class GeneratorOptionsTest(unittest.TestCase):

    def setUp(self):
        # Mock FileLoader to avoid FileNotFoundError
        with patch('pitaco.megasena.numbers_generator.MegasenaFileLoader') as MockLoader:
            mock_loader_instance = MockLoader.return_value
            mock_analyzer = MagicMock(spec=MegasenaResultsAnalyzer)
            mock_loader_instance.load_from_csv.return_value = mock_analyzer
            
            self.generator = MegasenaNumberGenerator("dummy_folder")
            self.analyzer = mock_analyzer
            
            # Setup default mock behaviors
            # 1. Mock Gap Distributions
            mock_gap_result = MagicMock()
            # 5 dicts for 5 gap positions
            mock_gap_result.sorted_distributions = [
                {1: 1.0}, # Pos 0 always 1
                {2: 1.0}, # Pos 1 always 2
                {3: 1.0}, # Pos 2 always 3
                {4: 1.0}, # Pos 3 always 4
                {5: 1.0}  # Pos 4 always 5
            ] 
            # Repetition stats: Force 'unique' for simplicity in tests
            mock_gap_result.repetition_stats = {"unique": 1.0, "one_pair": 0.0, "multiple_repetitions": 0.0}
            self.analyzer.get_sorted_gap_distributions.return_value = mock_gap_result

            # 2. Mock Frequency/Missing
            # Return some dummy list of (number, freq)
            self.analyzer.get_most_frequent.return_value = [(1, 10), (2, 5)]
            self.analyzer.get_numbers_by_absence_duration.return_value = [(3, 10), (4, 5)]

    def test_default_all_enabled(self):
        # Should call all update methods and use gaps
        with patch.object(self.generator, '_update_weights_based_on_frequency', wraps=self.generator._update_weights_based_on_frequency) as mock_freq:
            with patch.object(self.generator, '_update_weights_based_on_missing', wraps=self.generator._update_weights_based_on_missing) as mock_miss:
                with patch.object(self.generator, '_generate_with_gaps_and_weights', wraps=self.generator._generate_with_gaps_and_weights) as mock_gaps:
                    
                    draw = self.generator.generate(num_candidates=10)
                    
                    self.assertEqual(len(draw), 6)
                    mock_freq.assert_called_once()
                    mock_miss.assert_called_once()
                    mock_gaps.assert_called_once()
                    # Verify scoring was triggered in _generate_with_gaps_and_weights
                    _, kwargs = mock_gaps.call_args
                    self.assertTrue(kwargs.get('use_scoring'))

    def test_only_gaps(self):
        # Frequency and Missing should NOT be called
        with patch.object(self.generator, '_update_weights_based_on_frequency') as mock_freq:
            with patch.object(self.generator, '_update_weights_based_on_missing') as mock_miss:
                with patch.object(self.generator, '_generate_with_gaps_and_weights', wraps=self.generator._generate_with_gaps_and_weights) as mock_gaps_:
                     
                    draw = self.generator.generate(num_candidates=10, use_frequency=False, use_missing=False, use_gaps=True)
                    
                    self.assertEqual(len(draw), 6)
                    mock_freq.assert_not_called()
                    mock_miss.assert_not_called()
                    mock_gaps_.assert_called_once()
                     # Verify scoring was NOT keys in _generate_with_gaps_and_weights
                    _, kwargs = mock_gaps_.call_args
                    self.assertFalse(kwargs.get('use_scoring'))

    def test_only_frequency_no_gaps(self):
        # Gaps should NOT be called. _generate_with_weights_only SHOULD be called.
         with patch.object(self.generator, '_update_weights_based_on_frequency') as mock_freq:
            with patch.object(self.generator, '_update_weights_based_on_missing') as mock_miss:
                with patch.object(self.generator, '_generate_with_gaps_and_weights') as mock_gaps_method:
                    with patch.object(self.generator, '_generate_with_weights_only', return_value=[1,2,3,4,5,6]) as mock_weights_only:
                        
                        draw = self.generator.generate(num_candidates=10, use_frequency=True, use_missing=False, use_gaps=False)
                        
                        self.assertEqual(draw, [1,2,3,4,5,6])
                        mock_freq.assert_called_once()
                        mock_miss.assert_not_called()
                        mock_gaps_method.assert_not_called()
                        mock_weights_only.assert_called_once()

    def test_no_algorithms_defaults_weights_only(self):
        # If everything false, use_gaps=False branch -> _generate_with_weights_only (using base weights)
        with patch.object(self.generator, '_generate_with_weights_only', return_value=[1,2,3,4,5,6]) as mock_weights_only:
             self.generator.generate(use_frequency=False, use_missing=False, use_gaps=False)
             mock_weights_only.assert_called_once()

if __name__ == "__main__":
    unittest.main()
