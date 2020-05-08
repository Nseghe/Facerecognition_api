from flask import Flask
from application.config import Config
def create_app(config_class=Config):
	"""Construct the core application."""
	app = Flask(__name__)
	app.config.from_object(Config)
	with app.app_context():
		from application import api
		return app