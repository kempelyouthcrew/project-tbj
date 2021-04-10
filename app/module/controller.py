# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

from flask import render_template, request, redirect
from app import app
from .Model import db, SupplierDB, SparepartDetail, SparepartDB, QuotationDB, QuotationDetail, KonsumenDB, DODB, PODB, PODetail

@app.route('/dashboard', methods=['GET'])
def test():
    return render_template("dashboard.html")

@app.route('/input-konsumen', methods=['GET','POST'])
def input_konsumen():
    if request.method == 'POST':
        konsumen_id = request.form['konsumen_id']
        konsumen_name = request.form['konsumen_name']
        konsumen_address = request.form['konsumen_address']
        konsumen_phone = request.form['konsumen_phone']
        try:
            konsumen = KonsumenDB(konsumen_id=konsumen_id, 
                                konsumen_nama=konsumen_nama, 
                                konsumen_address=konsumen_address, 
                                konsumen_phone=konsumen_phone)
            db.session.add(konsumen)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
    listkonsumen = KonsumenDB.query.all()
    print(listkonsumen)
    return render_template("home.html", data=enumerate(listkonsumen,1))

@app.route('/update-konsumen/<int:id>')
def updateform_konsumen(id):
    konsumen = KonsumenDB.query.filter_by(id=id).first()
    return render_template("update.html", data=konsumen)

@app.route('/update-konsumen', methods=['POST'])
def update_konsumen():
    if request.method == 'POST':
        id = request.form['id']
        konsumen_id = request.form['konsumen_id']
        konsumen_name = request.form['konsumen_name']
        konsumen_address = request.form['konsumen_address']
        konsumen_phone = request.form['konsumen_phone']
        try:
            konsumen = Mahasiswa.query.filter_by(id=id).first()
            konsumen.konsumen_id=konsumen_id
            konsumen.konsumen_nama=konsumen_nama
            konsumen.konsumen_address=konsumen_address
            konsumen.konsumen_phone=konsumen_phone
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/input-konsumen")

@app.route('/delete-konsumen/<int:id>')
def delete_konsumen(id):
    try:
        konsumen = KonsumenDB.query.filter_by(id=id).first()
        db.session.delete(konsumen)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/input-konsumen")