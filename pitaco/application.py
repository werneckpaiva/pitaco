from flask.app import Flask
from flask import render_template
from flask import jsonify
from pitaco.megasena.numbers_generator import MegasenaNumberGenerator

app = Flask("pitaco")

@app.route('/')
def root():
    return  render_template("index.html")

@app.route('/generate')
def generate():
    generator = MegasenaNumberGenerator()
    numbers = generator.generate()
    return jsonify({'numbers':["%02d" % i for i in numbers]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)