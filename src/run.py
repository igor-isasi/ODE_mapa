from flask import Flask
from routes import routes
import uuid
import subprocess

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context=('/run/secrets/tls_cert','/run/secrets/tls_key'))