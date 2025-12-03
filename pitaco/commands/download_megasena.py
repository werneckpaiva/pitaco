import os
import logging
from os.path import join, dirname, abspath
from pitaco.megasena.file_loader import MegasenaFileLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOG = logging.getLogger(__name__)

def main():
    LOG.info("Starting Mega Sena download...")
    
    # pitaco/commands/download_megasena.py -> pitaco/commands -> pitaco -> root
    project_root = dirname(dirname(dirname(abspath(__file__))))
    folder = join(project_root, "downloads")
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    loader = MegasenaFileLoader(folder)
    
    LOG.info("Downloading file...")
    loader.download_file()
    
    LOG.info("Converting to CSV...")
    loader.convert_file_to_csv()
    
    LOG.info("Done!")

if __name__ == "__main__":
    main()
