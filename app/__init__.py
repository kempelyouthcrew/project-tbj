import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app.controller import *