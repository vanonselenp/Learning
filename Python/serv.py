from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello world"

@app.route('/test')
def test():
    x = {'a': 1, 'b': 2}
    return json.dumps(x)


if __name__ == '__main__':
    app.run()

