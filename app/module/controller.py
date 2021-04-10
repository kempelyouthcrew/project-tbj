# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

from flask import render_template, request, redirect
from app import app
from .Model import db, Mahasiswa
from flask_navigation import Navigation

nav = Navigation(app)
nav.Bar('leftbar', [
    nav.Item('Welcome', 'welcome', items=[
        nav.Item('Dashboard', 'dashboard'),
    ]),
    nav.Item('Data Master', 'data', items=[
        nav.Item('Konsumen', 'konsumen'),
        nav.Item('Sparepart', 'sparepart'),
        nav.Item('Supplier', 'supplier'),
    ]),
])

@app.route('/', methods=['GET'])
def index():
    return redirect("/dashboard")

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template("sites/dashboard.html")

@app.route('/konsumen', methods=['GET'])
def konsumen():
    listData = KonsumenDB.query.all()
    print(listData)
    return render_template("sites/konsumen/index.html", data=enumerate(listData,1))

@app.route('/sparepart', methods=['GET'])
def sparepart():
    return render_template("sites/konsumen/index.html")

@app.route('/supplier', methods=['GET'])
def supplier():
    return render_template("sites/konsumen/index.html")
