from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/inspire')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
    # app.run(debug=True)
