# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

from flask import render_template, request, redirect
from app import app
from .Model import db, SupplierDB, SparepartDetail, SparepartDB, QuotationDB, QuotationDetail, KonsumenDB, DODB, PODB, PODetail
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

# Dashboard
@app.route('/', methods=['GET'])
def index():
    return redirect("/dashboard")

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template("sites/dashboard.html")

# Konsumen
@app.route('/konsumen', methods=['GET'])
def konsumen():
    listKonsumen = KonsumenDB.query.all()
    print(listKonsumen)
    return render_template("sites/konsumen/index.html", data=enumerate(listKonsumen,1))

@app.route('/konsumen/add', methods=['GET'])
def konsumenAddForm():
    return render_template("sites/konsumen/addForm.html")

@app.route('/master/konsumen', methods=['GET'])
def konsumenMaster():
    konsumen = KonsumenDB.query.all()
    return json.dumps(KonsumenDB.serialize_list(konsumen))

@app.route('/konsumen/add', methods=['POST'])
def konsumenAdd():
    konsumen_id = request.form['konsumen_id']
    konsumen_name = request.form['konsumen_name']
    konsumen_address = request.form['konsumen_address']
    konsumen_phone = request.form['konsumen_phone']
    try:
        konsumen = KonsumenDB(konsumen_id=konsumen_id, 
                            konsumen_name=konsumen_name, 
                            konsumen_address=konsumen_address, 
                            konsumen_phone=konsumen_phone)
        db.session.add(konsumen)
        db.session.commit()
    except Exception as e:
        print("Failed to add data.")
        print(e)
    return render_template("sites/konsumen/addForm.html")

@app.route('/konsumen/edit/<int:id>', methods=['GET'])
def konsumenEditForm(id):
    konsumen = KonsumenDB.query.filter_by(id=id).first()
    return render_template("sites/konsumen/editForm.html", data=konsumen)

@app.route('/konsumen/edit', methods=['POST'])
def konsumenEdit():
    id = request.form['id']
    konsumen_id = request.form['konsumen_id']
    konsumen_name = request.form['konsumen_name']
    konsumen_address = request.form['konsumen_address']
    konsumen_phone = request.form['konsumen_phone']
    try:
        konsumen = KonsumenDB.query.filter_by(id=id).first()
        konsumen.konsumen_id=konsumen_id
        konsumen.konsumen_name=konsumen_name
        konsumen.konsumen_address=konsumen_address
        konsumen.konsumen_phone=konsumen_phone
        db.session.commit()
    except Exception as e:
        print("Failed to update data")
        print(e)
    return redirect("/konsumen")

@app.route('/konsumen/delete/<int:id>')
def deleteKonsumen(id):
    try:
        konsumen = KonsumenDB.query.filter_by(id=id).first()
        db.session.delete(konsumen)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/konsumen")

# Sparepart
@app.route('/sparepart', methods=['GET'])
def sparepart():
    listSparepart = SparepartDB.query.all()
    print(listSparepart)
    return render_template("sites/sparepart/index.html", data=enumerate(listSparepart,1))

@app.route('/sparepart/add', methods=['GET'])
def sparepartAddForm():
    return render_template("sites/sparepart/addForm.html")

@app.route('/sparepart/add', methods=['POST'])
def sparepartAdd():
    if request.method == 'POST':
        sparepart_name = request.form['sparepart_name']
        sparepart_number = request.form['sparepart_number']
        try:
            sparepart = SparepartDB(sparepart_name=sparepart_name, 
                                    sparepart_number=sparepart_number)
            db.session.add(sparepart)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
        return render_template("sites/sparepart/addForm.html")


@app.route('/sparepart/edit/<int:id>')
def sparepartEditForm(id):
    return render_template("sites/sparepart/editForm.html")

@app.route('/sparepart/edit', methods=['POST'])
def sparepartEdit():
    if request.method == 'POST':
        id = request.form['id']
        sparepart_name = request.form['sparepart_name']
        sparepart_number = request.form['sparepart_number']
        try:
            supplier = SupplierDB.query.filter_by(id=id).first()
            sparepart.sparepart_name=sparepart_name
            sparepart.sparepart_number=sparepart_number
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/sparepart")

@app.route('/sparepart/delete/<int:id>')
def sparepartDelete(id):
    try:
        sparepart = SparepartDB.query.filter_by(id=id).first()
        db.session.delete(sparepart)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/sparepart")

# Supplier
@app.route('/supplier', methods=['GET'])
def supplier():
    listSupplier = SupplierDB.query.all()
    print(listSupplier)
    return render_template("sites/supplier/index.html", data=enumerate(listSupplier,1))

@app.route('/supplier/add', methods=['GET'])
def supplierAddForm():
    return render_template("sites/supplier/addForm.html")

@app.route('/supplier/add', methods=['POST'])
def supplierAdd():
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']
        supplier_alamat = request.form['supplier_alamat']
        supplier_phone = request.form['supplier_phone']
        try:
            supplier = SupplierDB(supplier_name=supplier_name, 
                                supplier_alamat=supplier_alamat, 
                                supplier_phone=supplier_phone)
            db.session.add(supplier)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
        return render_template("sites/sparepart/addForm.html")


@app.route('/supplier/edit/<int:id>')
def supplierEditForm(id):
    supplier = SupplierDB.query.filter_by(id=id).first()
    return render_template("sites/supplier/editForm.html", data=supplier)

@app.route('/supplier/edit', methods=['POST'])
def supplierEdit():
    if request.method == 'POST':
        id = request.form['id']
        konsumen_id = request.form['konsumen_id']
        supplier_name = request.form['supplier_name']
        supplier_alamat = request.form['supplier_alamat']
        supplier_phone = request.form['supplier_phone']
        try:
            supplier = SupplierDB.query.filter_by(id=id).first()
            supplier.supplier_name=supplier_name
            supplier.supplier_alamat=supplier_alamat 
            supplier.supplier_phone=supplier_phone
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/supplier")

@app.route('/supplier/delete/<int:id>')
def supplierDelete(id):
    try:
        konsumen = KonsumenDB.query.filter_by(id=id).first()
        db.session.delete(konsumen)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/supplier")