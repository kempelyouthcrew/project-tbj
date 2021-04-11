# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

from flask import render_template, request, redirect, session, flash
from functools import wraps
from app import app
from .Model import db, SupplierDB, SparepartName, SparepartBrand, SparepartDB, QuotationDB, QuotationDetail, KonsumenDB, DODB, PODB, PODetail, UserManagementDB
from flask_navigation import Navigation
import bcrypt

nav = Navigation(app)
nav.Bar('leftbar', [
    nav.Item('Welcome', 'welcome', items=[
        nav.Item('Dashboard', 'dashboard'),
    ]),
    nav.Item('Purchasing', 'data', items=[
        nav.Item('Quotation', 'quotation'),
    ]),
    nav.Item('Data Master', 'data', items=[
        nav.Item('Konsumen', 'konsumen'),
        nav.Item('Supplier', 'supplier'),
        nav.Item('Sparepart', 'sparepart'),
        nav.Item('Sparepart Name', 'sparepartName'),
        nav.Item('Sparepart Brand', 'sparepartBrand'),
        nav.Item('User Management', 'usermanagement'),
    ]),
])

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            # flash('You need to login first')
            return redirect("/login")
    return wrap

# main
@app.route('/', methods=['GET'])
@login_required
def index():
    return redirect("/dashboard")

# Authentication
@app.route('/login', methods=['GET'])
def loginForm():
    return render_template("login/index.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password'].encode('utf-8')
    user = UserManagementDB.query.filter_by(user_email=email).first()
    if user:
        if bcrypt.hashpw(password, user.user_pass.encode('utf-8')) == user.user_pass.encode('utf-8'):
            session['name'] = user.user_name
            session['email'] = user.user_email
            session['level'] = user.user_level
            session['logged_in'] = True
            return redirect("/dashboard")
        else:
            return redirect("/login")
    else:
        return redirect("/login")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")

# Dashboard
@app.route('/dashboard', methods=['GET'])
@login_required
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
        return render_template("sites/supplier/addForm.html")


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

# Sparepart
@app.route('/sparepart', methods=['GET'])
def sparepart():
    listSparepart = SparepartDB.query.all()
    print(listSparepart)
    return render_template("sites/sparepart/index.html", data=enumerate(listSparepart,1))

@app.route('/sparepart/add', methods=['GET'])
def sparepartAddForm():
    listSparepartName = SparepartName.query.all()
    listSupplier = SupplierDB.query.all()
    listSparepartBrand = SparepartBrand.query.all()
    
    return render_template("sites/sparepart/addForm.html", listSparepartName=enumerate(listSparepartName), listSupplier=enumerate(listSupplier), listSparepartBrand=enumerate(listSparepartBrand))

@app.route('/sparepart/add', methods=['POST'])
def sparepartAdd():
    if request.method == 'POST':
        sparepart_name = request.form['sparepart_name']
        supplier_id = request.form['supplier_id']
        sparepart_number = request.form['sparepart_number']
        sparepart_brand = request.form['sparepart_brand']
        try:
            sparepart = SparepartDB(sparepart_name=sparepart_name, 
                                    sparepart_number=sparepart_number,
                                    sparepart_brand=sparepart_brand,
                                    supplier_id=supplier_id)
            db.session.add(sparepart)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
        return render_template("sites/sparepart/addForm.html")


@app.route('/sparepart/edit/<int:id>')
def sparepartEditForm(id):
    sparepart = SparepartDB.query.filter_by(id=id).first()
    listSparepartName = SparepartName.query.all()
    listSupplier = SupplierDB.query.all()
    listSparepartBrand = SparepartBrand.query.all()
    return render_template("sites/sparepart/editForm.html", data=sparepart, listSparepartName=enumerate(listSparepartName), listSupplier=enumerate(listSupplier), listSparepartBrand=enumerate(listSparepartBrand))

@app.route('/sparepart/edit', methods=['POST'])
def sparepartEdit():
    if request.method == 'POST':
        id = request.form['id']
        sparepart_name = request.form['sparepart_name']
        sparepart_number = request.form['sparepart_number']
        sparepart_brand = request.form['sparepart_brand']
        try:
            sparepart = SparepartDB.query.filter_by(id=id).first()
            sparepart.sparepart_name=sparepart_name
            sparepart.sparepart_number=sparepart_number
            sparepart.sparepart_brand=sparepart_brand
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

# SparepartName
@app.route('/sparepartName', methods=['GET'])
def sparepartName():
    listSparepartName = SparepartName.query.all()
    print(listSparepartName)
    return render_template("sites/sparepartName/index.html", data=enumerate(listSparepartName,1))

@app.route('/sparepartName/add', methods=['GET'])
def sparepartNameAddForm():
    return render_template("sites/sparepartName/addForm.html")

@app.route('/sparepartName/add', methods=['POST'])
def sparepartNameAdd():
    if request.method == 'POST':
        sparepart_name = request.form['sparepart_name']
        try:
            sparepartName = SparepartName(sparepart_name=sparepart_name)
            db.session.add(sparepartName)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
        return render_template("sites/sparepartName/addForm.html")


@app.route('/sparepartName/edit/<int:id>')
def sparepartNameEditForm(id):
    sparepart = SparepartName.query.filter_by(id=id).first()
    return render_template("sites/sparepartName/editForm.html", data=sparepart)

@app.route('/sparepartName/edit', methods=['POST'])
def sparepartNameEdit():
    if request.method == 'POST':
        id = request.form['id']
        sparepart_name = request.form['sparepart_name']
        try:
            sparepartName = SparepartName.query.filter_by(id=id).first()
            sparepartName.sparepart_name=sparepart_name
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/sparepartName")

@app.route('/sparepartName/delete/<int:id>')
def sparepartNameDelete(id):
    try:
        sparepartName = SparepartName.query.filter_by(id=id).first()
        db.session.delete(sparepartName)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/sparepartName")

# SparepartBrand
@app.route('/sparepartBrand', methods=['GET'])
def sparepartBrand():
    listSparepartBrand = SparepartBrand.query.all()
    print(listSparepartBrand)
    return render_template("sites/sparepartBrand/index.html", data=enumerate(listSparepartBrand,1))

@app.route('/sparepartBrand/add', methods=['GET'])
def sparepartBrandAddForm():
    return render_template("sites/sparepartBrand/addForm.html")

@app.route('/sparepartBrand/add', methods=['POST'])
def sparepartBrandAdd():
    if request.method == 'POST':
        sparepart_brand = request.form['sparepart_brand']
        try:
            sparepartBrand = SparepartBrand(sparepart_brand=sparepart_brand)
            db.session.add(sparepartBrand)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
        return render_template("sites/sparepartBrand/addForm.html")


@app.route('/sparepartBrand/edit/<int:id>')
def sparepartBrandEditForm(id):
    sparepart = SparepartBrand.query.filter_by(id=id).first()
    return render_template("sites/sparepartBrand/editForm.html", data=sparepart)

@app.route('/sparepartBrand/edit', methods=['POST'])
def sparepartBrandEdit():
    if request.method == 'POST':
        id = request.form['id']
        sparepart_brand = request.form['sparepart_brand']
        try:
            sparepartBrand = SparepartBrand.query.filter_by(id=id).first()
            sparepartBrand.sparepart_brand=sparepart_brand
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/sparepartBrand")

@app.route('/sparepartBrand/delete/<int:id>')
def sparepartBrandDelete(id):
    try:
        sparepartBrand = SparepartBrand.query.filter_by(id=id).first()
        db.session.delete(sparepartBrand)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/sparepartBrand")

# Quotation
@app.route('/quotation', methods=['GET'])
def quotation():
    listQuotation = QuotationDB.query.filter_by(id=id).first()
    listQuotation['detail'] = QuotationDetail.query.filter_by(id=id).first()
    print(listQuotation)
    return render_template("sites/quotation/index.html", data=enumerate(listQuotation,1))

@app.route('/quotation/add', methods=['GET'])
def quotationAddForm():
    return render_template("sites/quotation/addForm.html")

@app.route('/quotation/add', methods=['POST'])
def quotationAdd():
    quotation_date = request.form['quotation_date']
    konsumen_id = request.form['konsumen_id']
    quotation_number = request.form['quotation_number']
    sparepart_number = request.form['sparepart_number']
    sparepart_qty = request.form['sparepart_qty']
    sparepart_price = request.form['sparepart_price']
    try:
        quotation = QuotationDB(quotation_date=quotation_date,
                                konsumen_id=konsumen_id)
        quotation['detail'] = QuotationDetail(quotation_number=quotation_number,
                                sparepart_number=sparepart_number,
                                sparepart_qty=sparepart_qty,
                                sparepart_price=sparepart_price)
        db.session.add(quotation)
        db.session.commit()
    except Exception as e:
        print("Failed to add data.")
        print(e)
    return render_template("sites/quotation/addForm.html")

@app.route('/quotation/edit/<int:id>', methods=['GET'])
def quotationEditForm(id):
    quotation = QuotationDB.query.filter_by(id=id).first()
    quotation['detail'] = QuotationDetail.query.filter_by(id=id).first()
    return render_template("sites/quotation/editForm.html", data=quotation)

@app.route('/quotation/edit', methods=['POST'])
def quotationEdit():
    id = request.form['id']
    quotation_date = request.form['quotation_date']
    konsumen_id = request.form['konsumen_id']
    quotation_number = request.form['quotation_number']
    sparepart_number = request.form['sparepart_number']
    sparepart_qty = request.form['sparepart_qty']
    sparepart_price = request.form['sparepart_price']
    try:
        quotation = QuotationDB.query.filter_by(id=id).first()
        quotation['detail'] = QuotationDetail.query.filter_by(id=id).first()
        quotation.quotation_date=quotation_date
        quotation.konsumen_id=konsumen_id 
        quotation['detail'].quotation_number=quotation_number
        quotation['detail'].sparepart_number=sparepart_number
        quotation['detail'].sparepart_qty=sparepart_qty
        quotation['detail'].sparepart_price=sparepart_price
        db.session.commit()
    except Exception as e:
        print("Failed to update data")
        print(e)
    return redirect("/quotation")

@app.route('/quotation/delete/<int:id>')
def quotationKonsumen(id):
    try:
        quotation = QuotationDB.query.filter_by(id=id).first()
        quotation['detail'] = QuotationDetail.query.filter_by(id=id).first()
        db.session.delete(quotation)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/quotation")

@app.route('/quotation/info')
def quotationInfo():
    quotation = QuotationDB.query.filter_by(id=id).first()
    quotation['detail'] = QuotationDetail.query.filter_by(id=id).first()
    return render_template("sites/quotation/info.html")

# User Management
@app.route('/usermanagement', methods=['GET'])
def usermanagement():
    listUserManagement = UserManagementDB.query.all()
    print(listUserManagement)
    return render_template("sites/usermanagement/index.html", data=enumerate(listUserManagement,1))

@app.route('/usermanagement/add', methods=['GET'])
def usermanagementAddForm():
    return render_template("sites/usermanagement/addForm.html")

@app.route('/usermanagement/add', methods=['POST'])
def usermanagementAdd():
    user_name = request.form['user_name']
    user_email = request.form['user_email']
    user_pass = request.form['user_pass'].encode('utf-8')
    user_level = request.form['user_level']
    # password hash
    hash_password = bcrypt.hashpw(user_pass, bcrypt.gensalt())
    try:
        usermanagement = UserManagementDB(user_name=user_name, 
                            user_email=user_email, 
                            user_pass=hash_password, 
                            user_level=user_level)
        db.session.add(usermanagement)
        db.session.commit()
    except Exception as e:
        print("Failed to add data.")
        print(e)
    return render_template("sites/usermanagement/addForm.html")

@app.route('/usermanagement/edit/<int:id>', methods=['GET'])
def usermanagementEditForm(id):
    usermanagement = UserManagementDB.query.filter_by(id=id).first()
    return render_template("sites/usermanagement/editForm.html", data=usermanagement)

@app.route('/usermanagement/edit', methods=['POST'])
def usermanagementEdit():
    id = request.form['id']
    user_name = request.form['user_name']
    user_email = request.form['user_email']
    user_pass = request.form['user_pass'].encode('utf-8')
    user_level = request.form['user_level']
    # password hash
    hash_password = bcrypt.hashpw(user_pass, bcrypt.gensalt())
    try:
        usermanagement = UserManagementDB.query.filter_by(id=id).first()
        usermanagement.user_name=user_name
        usermanagement.user_email=user_email
        usermanagement.user_pass=hash_password
        usermanagement.user_level=user_level
        db.session.commit()
    except Exception as e:
        print("Failed to update data")
        print(e)
    return redirect("/usermanagement")

@app.route('/usermanagement/delete/<int:id>')
def deleteusermanagement(id):
    try:
        usermanagement = UserManagementDB.query.filter_by(id=id).first()
        db.session.delete(usermanagement)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/usermanagement")
