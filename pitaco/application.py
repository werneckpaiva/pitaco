from flask.app import Flask
from flask import render_template
from flask import jsonify
from pitaco.megasena.numbers_generator import MegasenaNumberGenerator
from pitaco.megasena.file_loader import MegasenaFileLoader
from os.path import dirname, join
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG = logging.getLogger(__name__)

app = Flask("pitaco")


@app.route('/')
def root():
    LOG.info("Root endpoint accessed")
    return  render_template("index.html")


@app.route('/generate')
def generate():
    folder = join(dirname(dirname(__file__)), "downloads")
    generator = MegasenaNumberGenerator(folder)
    numbers = generator.generate()
    return jsonify({'numbers':["%02d" % i for i in numbers]})


def get_analyzer():
    folder = join(dirname(dirname(__file__)), "downloads")
    loader = MegasenaFileLoader(folder)
    return loader.load_from_csv()


@app.route('/stats')
def stats():
    analyzer = get_analyzer()
    most_frequent = analyzer.get_most_frequent(10)
    longest_missing = analyzer.get_longest_numbers_missing(10)
    odd_even = analyzer.count_odd_even()
    
    return jsonify({
        'most_frequent': most_frequent,
        'longest_missing': longest_missing,
        'odd_even': odd_even
    })





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)