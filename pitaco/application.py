from flask.app import Flask
from flask import render_template
from flask import jsonify
from pitaco.megasena.numbers_generator import MegasenaNumberGenerator
from os.path import dirname, join


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





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)