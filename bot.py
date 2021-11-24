from flask import Flask
from flask import request
from OpenSSL import SSL

context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')

app = Flask(__name__)
sslify = SSLify(app)


@app.route('/inspire', methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        print(request.json)
    return {"ok": True}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=context)
    # app.run(debug=True)
