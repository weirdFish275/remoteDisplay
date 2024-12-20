from flask import Flask

app = Flask(__name__)

@app.route('/text')
def test():
    return "Hello"


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)