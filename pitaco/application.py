from flask.app import Flask
from flask import render_template

app = Flask("pitaco")

@app.route('/')
def root():
    return  render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)