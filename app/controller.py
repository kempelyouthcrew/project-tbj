# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

from flask import render_template, request, redirect
from app import app
from .Model import db, Mahasiswa

@app.route('/dashboard', methods=['GET'])
def test():
    return render_template("dashboard.html")

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        try:
            mhs = Mahasiswa(nim=nim, nama=nama)
            db.session.add(mhs)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
    listMhs = Mahasiswa.query.all()
    print(listMhs)
    return render_template("home.html", data=enumerate(listMhs,1))

@app.route('/form-update/<int:id>')
def updateForm(id):
    mhs = Mahasiswa.query.filter_by(id=id).first()
    return render_template("update.html", data=mhs)

@app.route('/form-update', methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        nim = request.form['nim']
        try:
            mhs = Mahasiswa.query.filter_by(id=id).first()
            mhs.nama = nama
            mhs.nim = nim
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/")

@app.route('/delete/<int:id>')
def delete(id):
    try:
        mhs = Mahasiswa.query.filter_by(id=id).first()
        db.session.delete(mhs)
        db.session.commit()
    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/")