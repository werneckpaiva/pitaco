import unittest
from pitaco.megasena.file_loader import MegasenaFileLoader
from os.path import dirname, join
import os


class Test(unittest.TestCase):

    FOLDER = join(dirname(dirname(dirname(dirname(__file__)))), "downloads_tests")

    def test_extract_file(self):
        f = join(self.FOLDER, "D_MEGA.HTM")
        if os.path.isfile(f):
            os.remove(f)

        self.assertFalse(os.path.isfile(f))
        loader = MegasenaFileLoader(self.FOLDER)
        loader.extract_file()
        self.assertTrue(os.path.isfile(f))

    def test_convert_html_to_csv(self):
        f = join(self.FOLDER, "result.csv")
        if os.path.isfile(f):
            os.remove(f)

        self.assertFalse(os.path.isfile(f))
        loader = MegasenaFileLoader(self.FOLDER)
        loader.convert_file_to_csv()
        self.assertTrue(os.path.isfile(f))

    def test_load_from_csv(self):
        loader = MegasenaFileLoader(self.FOLDER)
        megasena = loader.load_from_csv()

        self.assertEquals(len(megasena.results), 1766)

        self.assertEqual(megasena.results[-1].n, '1766')
        self.assertEqual(megasena.results[-1].numbers, [60, 23, 22, 46, 53, 41])

        self.assertEqual(megasena.results[-2].n, '1765')
        self.assertEqual(megasena.results[-2].numbers, [1, 28, 56, 37, 6, 58])
