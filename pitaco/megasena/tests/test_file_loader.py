import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import tempfile
import pandas as pd
from datetime import datetime
from pitaco.megasena.file_loader import MegasenaFileLoader

class TestMegasenaFileLoader(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.loader = MegasenaFileLoader(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    @patch('urllib.request.build_opener')
    def test_download_file(self, mock_build_opener):
        # Mock the response from urllib
        mock_response = MagicMock()
        mock_response.read.side_effect = [b'chunk1', b'chunk2', b'']
        mock_response.__enter__.return_value = mock_response
        
        mock_opener = MagicMock()
        mock_opener.open.return_value = mock_response
        mock_build_opener.return_value = mock_opener

        self.loader.download_file()

        target_file = os.path.join(self.test_dir.name, MegasenaFileLoader.XLSX_FILE)
        self.assertTrue(os.path.exists(target_file))
        with open(target_file, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'chunk1chunk2')

    @patch('pandas.read_excel')
    def test_convert_file_to_csv(self, mock_read_excel):
        # Create a sample DataFrame
        data = {
            'Concurso': [1, 2],
            'Data do Sorteio': [datetime(2023, 1, 1), '02/01/2023'],
            'Bola1': [1, 7],
            'Bola2': [2, 8],
            'Bola3': [3, 9],
            'Bola4': [4, 10],
            'Bola5': [5, 11],
            'Bola6': [6, 12]
        }
        df = pd.DataFrame(data)
        mock_read_excel.return_value = df

        # Create a dummy XLSX file (content doesn't matter because we mock read_excel)
        xlsx_path = os.path.join(self.test_dir.name, MegasenaFileLoader.XLSX_FILE)
        with open(xlsx_path, 'w') as f:
            f.write('dummy')

        self.loader.convert_file_to_csv()

        csv_path = os.path.join(self.test_dir.name, MegasenaFileLoader.CSV_FILE)
        self.assertTrue(os.path.exists(csv_path))

        # Verify CSV content
        with open(csv_path, 'r', encoding='utf-8') as f:
            content = f.read().strip().split('\n')
            self.assertEqual(len(content), 2)
            self.assertEqual(content[0], '1,2023-01-01,01,02,03,04,05,06')
            self.assertEqual(content[1], '2,2023-01-02,07,08,09,10,11,12')

    def test_load_from_csv(self):
        # Create a sample CSV file
        csv_path = os.path.join(self.test_dir.name, MegasenaFileLoader.CSV_FILE)
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write('1,2023-01-01,01,02,03,04,05,06\n')
            f.write('2,2023-01-02,07,08,09,10,11,12\n')

        analyzer = self.loader.load_from_csv()

        self.assertEqual(len(analyzer.results), 2)
        
        res1 = analyzer.results[0]
        self.assertEqual(res1.n, '1')
        self.assertEqual(res1.dt, datetime(2023, 1, 1))
        self.assertEqual(res1.numbers, [1, 2, 3, 4, 5, 6])

        res2 = analyzer.results[1]
        self.assertEqual(res2.n, '2')
        self.assertEqual(res2.dt, datetime(2023, 1, 2))
        self.assertEqual(res2.numbers, [7, 8, 9, 10, 11, 12])

if __name__ == '__main__':
    unittest.main()
