from flask.app import Flask

app = Flask("pitaco")

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()