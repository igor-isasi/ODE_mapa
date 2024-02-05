from flask import Flask
from routes import routes
import uuid

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = uuid.uuid4().hex
app.register_blueprint(routes)