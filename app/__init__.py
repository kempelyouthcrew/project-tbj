import os
from flask import Flask
from flask_navigation import Navigation
from config import Config
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
nav = Navigation(app)
# app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/testflask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://u5073922_tbjuser_0:D,q-DGb;Bny]@teknikberlianjaya.com/u5073922_tbjlive_0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from app.module.controller import *