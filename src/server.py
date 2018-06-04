from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world!!'


@app.route('/ping')
def ping():
    return 'pang'


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
