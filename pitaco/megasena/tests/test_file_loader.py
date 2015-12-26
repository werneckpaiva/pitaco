import unittest
from pitaco.megasena.file_loader import MegasenaFileLoader
from os.path import dirname, join
import os


class Test(unittest.TestCase):

    FOLDER = join(dirname(dirname(dirname(dirname(__file__)))), "downloads_tests")

    def testExtractFile(self):
        f = join(self.FOLDER, "D_MEGA.HTM")
        if os.path.isfile(f):
            os.remove(f)

        self.assertFalse(os.path.isfile(f))
        loader = MegasenaFileLoader(self.FOLDER)
        loader.extract_file()
        self.assertTrue(os.path.isfile(f))

    def testConvertHtmlToCsv(self):
        f = join(self.FOLDER, "result.csv")
        if os.path.isfile(f):
            os.remove(f)

        self.assertFalse(os.path.isfile(f))
        loader = MegasenaFileLoader(self.FOLDER)
        loader.convert_file_to_csv()
        self.assertTrue(os.path.isfile(f))