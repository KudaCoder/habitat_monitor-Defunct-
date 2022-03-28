from flask import Flask

from . import blueprints, models
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

models.init_app(app)

app.register_blueprint(blueprints.api.bp)
