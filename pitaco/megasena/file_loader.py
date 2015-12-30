import urllib2
import zipfile
from os.path import join
from datetime import datetime
from lxml.html import fromstring
from pitaco.megasena.results_analyzer import MegasenaResultsAnalyzer


class MegasenaFileLoader(object):

    URL = "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip"
    download_folder = None

    def __init__(self, download_folder):
        self.download_folder = download_folder

    def _get_download_filename(self):
        return join(self.download_folder, "megasena.zip")

    def download_file(self):
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', 'security=true'))
        r = opener.open(self.URL)
        block_size = 8192
        with open(self._get_download_filename(), "wb") as f:
            while True:
                chunk = r.read(block_size)
                if not chunk: break
                f.write(chunk)

    def extract_file(self):
        with zipfile.ZipFile(self._get_download_filename(), "r") as z:
            z.extractall(self.download_folder)

    def convert_file_to_csv(self):
        filename = join(self.download_folder, "D_MEGA.HTM") 
        with open(filename, "r") as f:
            content = f.read()
        html = fromstring(content)
        rows = html.cssselect('tr')
        result = []
        for row in rows:
            tds = row.cssselect("td")
            if len(tds) == 21:
                numbers = [t.text for t in tds[2:8]]
                dt = datetime.strptime(tds[1].text, "%d/%m/%Y")
                result.append((tds[0].text, dt, numbers))

        sorted(result, key=lambda r: r[0])
        last = result[-1]
        csv_filename = join(self.download_folder, "result.csv") 
        with open(csv_filename, "w") as f:
            for r in result[0:-1]:
                f.write("%s,%s,%s\n" % (r[0], r[1].strftime("%Y-%m-%d"), ",".join([str(n) for n in r[2]])))
            f.write("%s,%s,%s" % (last[0], last[1].strftime("%Y-%m-%d"), ",".join([str(n) for n in last[2]])))

    def load_from_csv(self):
        megasena = MegasenaResultsAnalyzer()
        csv_filename = join(self.download_folder, "result.csv")
        for line in open(csv_filename, "r"):
            parts = line.split(",")
            n = parts[0]
            dt = datetime.strptime(parts[1], "%Y-%m-%d")
            numbers = parts[2:8]
            megasena.add_result(
                n=n,
                dt=dt,
                numbers=numbers
            )
        return megasena
