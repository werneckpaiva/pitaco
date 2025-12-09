import csv
import zipfile
import urllib.request
import urllib.error
from os.path import join
from datetime import datetime
from typing import List, Tuple, Optional

import pandas as pd
import logging
from pitaco.megasena.results_analyzer import MegasenaResultsAnalyzer
from functools import lru_cache as cache

LOG = logging.getLogger(__name__)

class MegasenaFileLoader:
    """
    Handles downloading, extracting, and loading Mega Sena results.
    """

    # TODO: Verify the correct URL. 'view-source:' is invalid.
    # If the target is a ZIP file, use the ZIP URL.
    # If it's an API returning JSON (modern Caixa), this entire approach needs updating.
    # For now, assuming a direct HTML or ZIP download URL.
    URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados/download?modalidade=Mega-Sena"
    
    RESULT_FILENAME = "megasena_result" # Base name
    XLSX_FILE = "megasena_result.xlsx"
    CSV_FILE = "result.csv"

    def __init__(self, download_folder: str):
        self.download_folder = download_folder

    def _get_file_path(self, filename: str) -> str:
        return join(self.download_folder, filename)

    def download_file(self) -> None:
        """Downloads the results file from the configured URL."""
        opener = urllib.request.build_opener()
        opener.addheaders.append(('Cookie', 'security=true'))
        opener.addheaders.append(('User-Agent', 'Mozilla/5.0')) # Often needed

        try:
            with opener.open(self.URL) as response:
                target_file = self._get_file_path(self.XLSX_FILE)

                with open(target_file, "wb") as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                LOG.info(f"Downloaded to {target_file}")
        except urllib.error.URLError as e:
            LOG.error(f"Error downloading file: {e}")

    def extract_file(self) -> None:
        """Extracts the downloaded ZIP file. (Deprecated for XLSX)"""
        pass

    def convert_file_to_csv(self) -> None:
        """Parses the XLSX result file and converts it to CSV."""
        xlsx_path = self._get_file_path(self.XLSX_FILE)
        csv_path = self._get_file_path(self.CSV_FILE)
        
        try:
            df = pd.read_excel(xlsx_path)
        except FileNotFoundError:
            LOG.error(f"File not found: {xlsx_path}")
            return
        except Exception as e:
            LOG.error(f"Error reading excel file: {e}")
            return

        # Ensure columns exist
        required_columns = ['Concurso', 'Data do Sorteio', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
        if not all(col in df.columns for col in required_columns):
            LOG.error(f"Missing columns in XLSX. Available: {df.columns}")
            return

        # Sort by Concurso
        df['Concurso'] = pd.to_numeric(df['Concurso'], errors='coerce')
        df = df.sort_values('Concurso')

        with open(csv_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for _, row in df.iterrows():
                try:
                    concurso = str(int(row['Concurso']))
                    # Date might be datetime or string
                    dt = row['Data do Sorteio']
                    if isinstance(dt, str):
                        dt_obj = datetime.strptime(dt, "%d/%m/%Y")
                    else:
                        dt_obj = dt
                    
                    dt_str = dt_obj.strftime("%Y-%m-%d")
                    
                    numbers = [
                        str(row['Bola1']), str(row['Bola2']), str(row['Bola3']),
                        str(row['Bola4']), str(row['Bola5']), str(row['Bola6'])
                    ]
                    # Pad numbers with 0 if needed (assuming they are ints)
                    numbers = [n.zfill(2) for n in numbers]

                    writer.writerow([concurso, dt_str] + numbers)
                except Exception as e:
                    LOG.error(f"Error processing row {row}: {e}")
        
        LOG.info(f"Converted to {csv_path}")

    @cache
    def load_from_csv(self) -> MegasenaResultsAnalyzer:
        """Loads results from CSV into the analyzer."""
        megasena = MegasenaResultsAnalyzer()
        csv_path = self._get_file_path(self.CSV_FILE)
        
        try:
            with open(csv_path, "r", encoding='utf-8') as f:
                reader = csv.reader(f)
                for parts in reader:
                    if not parts: continue
                    n = parts[0]
                    dt = datetime.strptime(parts[1], "%Y-%m-%d")
                    numbers = parts[2:8]
                    megasena.add_result(n=n, dt=dt, numbers=numbers)
        except FileNotFoundError:
            LOG.error(f"CSV file not found: {csv_path}")
            
        return megasena
