from flask.app import Flask
from flask import render_template
from flask import jsonify
from pitaco.megasena.numbers_generator import MegasenaNumberGenerator
from pitaco.megasena.file_loader import MegasenaFileLoader
from os.path import dirname, join
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG = logging.getLogger(__name__)

app = Flask("pitaco")


@app.route('/')
def root():
    LOG.info("Root endpoint accessed")
    ga_tracking_id = os.environ.get('GA_TRACKING_ID')
    LOG.info("GA Tracking ID: %s", ga_tracking_id)
    return render_template("index.html", ga_tracking_id=ga_tracking_id)


from flask import request

@app.route('/generate')
def generate():
    folder = join(dirname(dirname(__file__)), "downloads")
    
    use_frequency = request.args.get('use_frequency', 'true') == 'true'
    use_missing = request.args.get('use_missing', 'true') == 'true'
    use_gaps = request.args.get('use_gaps', 'true') == 'true'
    
    generator = MegasenaNumberGenerator(folder)
    numbers = generator.generate(
        use_frequency=use_frequency,
        use_missing=use_missing,
        use_gaps=use_gaps
    )
    return jsonify({'numbers':["%02d" % i for i in numbers]})


def get_analyzer():
    folder = join(dirname(dirname(__file__)), "downloads")
    loader = MegasenaFileLoader(folder)
    return loader.load_from_csv()


@app.route('/stats')
def stats():
    analyzer = get_analyzer()
    most_frequent = analyzer.get_most_frequent(60)
    longest_missing = analyzer.get_numbers_by_absence_duration(60)
    result = analyzer.get_sorted_gap_distributions()
    
    # gap_dist is a list of dicts.
    # We need to format it for JSON.
    # Let's return list of lists of items [gap, val]
    sorted_gap_dists = [sorted(g.items()) for g in result.sorted_distributions]

    return jsonify({
        'most_frequent': most_frequent,
        'longest_missing': longest_missing,
        'gap_distribution': sorted_gap_dists
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)