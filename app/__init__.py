import os
from flask import Flask
from flask_navigation import Navigation
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
nav = Navigation(app)
app.secret_key = 'teknikberlianjaya123tbjadministrator'
# app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/testflask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u5073922_tbjuser_0:D,q-DGb;Bny]@teknikberlianjaya.com/u5073922_tbjlive_0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size' : 300, 'pool_recycle' : 7200, 'pool_pre_ping': True}
db = SQLAlchemy(app)
with app.app_context():
    db.init_app(app)
CORS(app)
from app.module.controller import *