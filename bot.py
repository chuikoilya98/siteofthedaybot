from flask import Flask
from flask import request
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)


@app.route('/inspire', methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        print(request.json)
    return {"ok": True}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
    # app.run(debug=True)
