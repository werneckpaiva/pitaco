from flask.app import Flask
from flask import render_template
from flask import jsonify
from pitaco.megasena.numbers_generator import MegasenaNumberGenerator
from os.path import dirname, join
from pitaco.megasena.file_loader import MegasenaFileLoader

app = Flask("pitaco")


@app.route('/')
def root():
    return  render_template("index.html")


@app.route('/generate')
def generate():
    folder = join(dirname(dirname(__file__)), "downloads")
    generator = MegasenaNumberGenerator(folder)
    numbers = generator.generate()
    return jsonify({'numbers':["%02d" % i for i in numbers]})


@app.route('/_download')
def download():
    folder = join(dirname(dirname(__file__)), "downloads")
    loader = MegasenaFileLoader(folder)
    loader.download_file()
    loader.extract_file()
    loader.convert_file_to_csv()
    return "Ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)