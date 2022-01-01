import zipfile
from os.path import join
from datetime import datetime
from lxml.html import fromstring
from pitaco.megasena.results_analyzer import MegasenaResultsAnalyzer
import urllib.request


class MegasenaFileLoader(object):

    URL = "view-source:https://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/"
    RESULT_FILE = "resultado_megasena.html"
    download_folder = None

    def __init__(self, download_folder):
        self.download_folder = download_folder

    def _get_download_filename(self):
        return join(self.download_folder, "megasena_result.html")

    def download_file(self):
        opener = urllib.request.build_opener()
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
        filename = join(self.download_folder, MegasenaFileLoader.RESULT_FILE)
        with open(filename, "r", encoding="ISO-8859-1") as f:
            content = f.read()
        html = fromstring(content)
        rows = html.cssselect('tr')
        result = []
        for row in rows:
            tds = row.cssselect("td")
            if len(tds) > 10:
                numbers = [t.text for t in tds[3:9]]
                dt = datetime.strptime(tds[2].text, "%d/%m/%Y")
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
