from flask import Flask
from config import Config

app = Flask(__name__, static_url_path='', static_folder='uploads')
app.config.from_object(Config)

from app import routes

# {{url_for('uploads', filename='{{file_path}}')}}
