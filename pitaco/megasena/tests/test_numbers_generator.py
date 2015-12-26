import unittest
from pitaco.megasena.numbers_generator import MegasenaNumberGenerator


class NumbersGeneratorTest(unittest.TestCase):


    def test_generate_6_numbers(self):
        generator = MegasenaNumberGenerator()
        numbers = generator.generate()
        self.assertEqual(6, len(numbers))


if __name__ == "__main__":
    unittest.main()