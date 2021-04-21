import os
from flask import render_template, request, redirect, session, flash, make_response, url_for
from functools import wraps
from app import app
from .Model import db, SupplierDB, SparepartName, SparepartBrand, SparepartDB, QuotationDB, QuotationDetail, KonsumenDB, DODB, DODetail, PODB, UserManagementDB, POKeluarDB, POKeluarDetail, InvoiceDB
from flask_navigation import Navigation
import bcrypt
import json
import random
import decimal, datetime
from sqlalchemy.sql import text
from flask_weasyprint import HTML, render_pdf

nav = Navigation(app)
nav.Bar('leftbar', [
    nav.Item('Welcome', 'welcome', items=[
        nav.Item('Dashboard', 'dashboard'),
    ]),
    nav.Item('Purchasing', 'data', items=[
        nav.Item('Quotation', 'quotation'),
        nav.Item('PO Masuk', 'pokonsumen'),
        nav.Item('Delivery Order', 'do'),
        nav.Item('Invoice', 'invoice'),
        nav.Item('PO Keluar', 'pokeluar'),
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

#alchemyEncoder for json
def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

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

@app.route('/konsumen/add', methods=['POST'])
def konsumenAdd():
    konsumen_name = request.form['konsumen_name']
    konsumen_address = request.form['konsumen_address']
    konsumen_phone = request.form['konsumen_phone']

    phrase = (konsumen_name.replace('PT', '')).split()
    acronym = ""
    phraseCount = len(phrase)
    i = 0

    if phraseCount == 1:
        while i < phraseCount:
            acronym = acronym + phrase[i][0].upper()
            acronym = acronym + phrase[i][1].upper()
            acronym = acronym + phrase[i][2].upper()
            i += 1
    elif phraseCount == 2:
        while i < phraseCount:
            acronym = acronym + phrase[i][0].upper()
            i += 1
            if i == phraseCount:
                acronym = acronym + phrase[1][1].upper()                
    else:
        while i < phraseCount:
            acronym = acronym + phrase[i][0].upper()
            i += 1
        
    try:
        konsumen = KonsumenDB(konsumen_id=acronym, 
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
    listSparepart = SparepartDB.query\
        .join(SparepartName, SparepartDB.sparepart_name==SparepartName.id)\
        .join(SparepartBrand, SparepartDB.sparepart_brand==SparepartBrand.id)\
        .join(SupplierDB, SparepartDB.supplier_id==SupplierDB.id)\
        .add_columns(SparepartDB.id,\
            SparepartDB.sparepart_number,\
            SparepartName.sparepart_name,\
            SparepartBrand.sparepart_brand,\
            SupplierDB.supplier_name\
        )
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
        sparepart_price = request.form['sparepart_price']
        try:
            sparepart = SparepartDB(sparepart_name=sparepart_name, 
                                    sparepart_number=sparepart_number,
                                    sparepart_brand=sparepart_brand,
                                    supplier_id=supplier_id,
                                    sparepart_price=sparepart_price)
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
        sparepart_price = request.form['sparepart_price']
        try:
            sparepart = SparepartDB.query.filter_by(id=id).first()
            sparepart.sparepart_name=sparepart_name
            sparepart.sparepart_number=sparepart_number
            sparepart.sparepart_brand=sparepart_brand
            sparepart.sparepart_price=sparepart_price
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
    listQuotation = QuotationDB.query.join(KonsumenDB, QuotationDB.konsumen_id==KonsumenDB.id)\
        .add_columns(QuotationDB.id, QuotationDB.quotation_date, QuotationDB.quotation_number, KonsumenDB.konsumen_name,  QuotationDB.quotation_validity)

    print(listQuotation)
    return render_template("sites/quotation/index.html", listQuotation=enumerate(listQuotation))

@app.route('/quotation/add', methods=['GET'])
def quotationAddForm():
    listSparepart = SparepartDB.query.all()
    listKonsumen = KonsumenDB.query.all()
    return render_template("sites/quotation/addForm.html", listSparepart=listSparepart, listKonsumen=enumerate(listKonsumen))

@app.route('/quotation/add', methods=['POST'])
def quotationAdd():
    dateNow = datetime.datetime.now()
    quotation_date = dateNow
    quotation_number = 'QUO.TBJ-' + str(random.randint(1000, 9999))
    quotation_validity = 1
    formCount = request.form['formCount']
    konsumen_id = request.form['konsumen_id']
    quotation_price = request.form['sum_price']
    quotation_ppn = request.form['ppn']
    quotation_materai = request.form['materai']
    quotation_totalprice = request.form['grandprice']
    idParent = ""

    try:
        quotation = QuotationDB(quotation_date=quotation_date,
                                quotation_number=quotation_number,
                                quotation_validity=quotation_validity,
                                konsumen_id=konsumen_id,
                                quotation_price=quotation_price,
                                quotation_ppn=quotation_ppn,
                                quotation_materai=quotation_materai,
                                quotation_totalprice=quotation_totalprice)
        db.session.add(quotation)
        db.session.commit()
        db.session.flush()  
        idParent = quotation.id
        
    except Exception as e:
        print("Failed to add data.")
        print(e)

    i = 0
    while i < int(formCount):
        i = i + 1
        if 'sparepart_'+ str(i) in request.form:
            quotation_id = idParent
            sparepart_number = request.form['sparepart_'+ str(i)]
            sparepart_qty = request.form['qty_'+ str(i)]
            sparepart_price = request.form['price_'+ str(i)]
            sparepart_totalprice = request.form['total_price_'+ str(i)]
            sparepart_description = request.form['description_'+ str(i)]
            try:
                quotationDet = QuotationDetail(quotation_id=quotation_id,
                                    sparepart_number=sparepart_number,
                                    sparepart_qty=sparepart_qty,
                                    sparepart_price=sparepart_price,
                                    sparepart_totalprice=sparepart_totalprice,
                                    sparepart_description=sparepart_description)
                db.session.add(quotationDet)
                db.session.commit()
            except Exception as e:
                print("Failed to add data.")
                print(e)

    generatePDF('tes','quotation','quotdata')
    return render_template("sites/quotation/addForm.html")

@app.route('/quotation/info/<int:id>', methods=['GET'])
def quotationInfo(id):
    quotation = QuotationDetail.query\
        .join(QuotationDB, QuotationDB.id==QuotationDetail.quotation_id)\
        .filter_by(id=id)\
        .join(KonsumenDB, QuotationDB.konsumen_id==KonsumenDB.id)\
        .join(SparepartDB, QuotationDetail.sparepart_number==SparepartDB.id)\
        .join(SparepartName, SparepartDB.sparepart_name==SparepartName.id)\
        .join(SparepartBrand, SparepartDB.sparepart_brand==SparepartBrand.id)\
        .add_columns(\
            QuotationDB.id,\
            QuotationDB.quotation_date,\
            QuotationDB.quotation_number,\
            QuotationDB.quotation_price,\
            QuotationDB.quotation_ppn,\
            QuotationDB.quotation_materai,\
            QuotationDB.quotation_totalprice,\
            QuotationDB.quotation_validity,\
            SparepartDB.sparepart_number,\
            SparepartName.sparepart_name,\
            QuotationDetail.sparepart_qty,\
            QuotationDetail.sparepart_price,\
            QuotationDetail.sparepart_totalprice,\
            QuotationDB.quotation_number,\
            KonsumenDB.konsumen_address,\
            KonsumenDB.konsumen_name\
        )\
        .all()
    print(quotation)
    return render_template("sites/quotation/info.html", quotation=quotation)


# PO Keluar
@app.route('/pokeluar', methods=['GET'])
def pokeluar():
    listPOKeluar = POKeluarDB.query\
                    .join(PODB, PODB.id==POKeluarDB.po_id)\
                    .join(SupplierDB, SupplierDB.id==POKeluarDB.supplier_id)\
                    .add_columns(\
                        POKeluarDB.id,\
                        POKeluarDB.pokeluar_date,\
                        POKeluarDB.pokeluar_number,\
                        PODB.po_number,\
                        SupplierDB.supplier_name,\
                        )
    
    return render_template("sites/pokeluar/index.html", listPOKeluar=enumerate(listPOKeluar))

@app.route('/pokeluar/add', methods=['GET'])
def pokeluarAddForm():
    listSparepart = SparepartDB.query.all()
    listPo = PODB.query.all()
    listSupplier = SupplierDB.query.all()
    return render_template("sites/pokeluar/addForm.html", listSparepart=listSparepart, listPo=listPo, listSupplier=listSupplier)

@app.route('/pokeluar/add', methods=['POST'])
def pokeluarAdd():
    dateNow = datetime.datetime.now()
    pokeluar_date = dateNow
    pokeluar_number = 'PO.TBJ-' + str(random.randint(1000, 9999))
    formCount = request.form['formCount']
    supplier_id = request.form['supplier_name']
    po_id = request.form['po_number']
    pokeluar_price = request.form['sum_price']
    idParent = ""

    try:
        pokeluar = POKeluarDB(pokeluar_number=pokeluar_number,
                            pokeluar_date=pokeluar_date,
                            supplier_id=supplier_id,
                            po_id=po_id,
                            pokeluar_price=pokeluar_price)
        db.session.add(pokeluar)
        db.session.commit()
        db.session.flush()  
        idParent = pokeluar.id
        
    except Exception as e:
        print("Failed to add data.")
        print(e)

    i = 0
    while i < int(formCount):
        i = i + 1
        if 'sparepart_'+ str(i) in request.form:
            pokeluar_id = idParent
            sparepart_number = request.form['sparepart_'+ str(i)]
            sparepart_qty = request.form['qty_'+ str(i)]
            sparepart_price = request.form['price_'+ str(i)]
            sparepart_totalprice = request.form['total_price_'+ str(i)]
            try:
                pokeluarDet = POKeluarDetail(pokeluar_id=pokeluar_id,
                                    sparepart_number=sparepart_number,
                                    sparepart_qty=sparepart_qty,
                                    sparepart_price=sparepart_price,
                                    sparepart_totalprice=sparepart_totalprice)
                db.session.add(pokeluarDet)
                db.session.commit()
            except Exception as e:
                print("Failed to add data.")
                print(e)

    return render_template("sites/pokeluar/addForm.html")


@app.route('/pokeluar/info/<int:id>', methods=['GET'])
def pokeluarInfo(id):
    pokeluar = POKeluarDetail.query\
        .join(POKeluarDB, POKeluarDB.id==POKeluarDetail.pokeluar_id)\
        .filter_by(id=id)\
        .join(SupplierDB, POKeluarDB.supplier_id==SupplierDB.id)\
        .join(SparepartDB, POKeluarDetail.sparepart_number==SparepartDB.id)\
        .join(SparepartName, SparepartDB.sparepart_name==SparepartName.id)\
        .join(SparepartBrand, SparepartDB.sparepart_brand==SparepartBrand.id)\
        .add_columns(\
            POKeluarDB.id,\
            POKeluarDB.pokeluar_date,\
            POKeluarDB.pokeluar_number,\
            POKeluarDB.pokeluar_price,\
            SparepartDB.sparepart_number,\
            SparepartName.sparepart_name,\
            POKeluarDetail.sparepart_qty,\
            POKeluarDetail.sparepart_price,\
            POKeluarDetail.sparepart_totalprice,\
            POKeluarDB.po_id,\
            SupplierDB.supplier_alamat,\
            SupplierDB.supplier_name\
        )\
        .all()
    print(pokeluar)
    return render_template("sites/pokeluar/info.html", pokeluar=pokeluar)



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

# PO Konsumen
@app.route('/pokonsumen', methods=['GET'])
def pokonsumen():
    listPOKonsumen = PODB.query\
        .join(QuotationDB, PODB.quotation_id==QuotationDB.id)\
        .join(KonsumenDB, QuotationDB.konsumen_id==KonsumenDB.id)\
        .add_columns(PODB.id, PODB.po_date, PODB.po_number, KonsumenDB.konsumen_name, PODB.po_number)

    print(listPOKonsumen)
    return render_template("sites/pokonsumen/index.html", listPOKonsumen=enumerate(listPOKonsumen))

@app.route('/pokonsumen/add', methods=['GET'])
def pokonsumenAddForm():
    listSparepart = SparepartDB.query.all()
    listKonsumen = KonsumenDB.query.all()
    return render_template("sites/pokonsumen/addForm.html", listSparepart=listSparepart, listKonsumen=enumerate(listKonsumen))

@app.route('/pokonsumen/add', methods=['POST'])
def pokonsumenAdd():
    dateNow = datetime.datetime.now()
    po_date = dateNow
    quotation_id = request.form['quotation']
    seller_name = request.form['seller']
    po_number = request.form['reference']

    try:
        po = PODB(po_date=po_date,
                quotation_id=quotation_id,
                po_number=po_number,
                seller_name=seller_name)
        db.session.add(po)
        db.session.commit()
        db.session.flush()  
        idParent = po.id
        
    except Exception as e:
        print("Failed to add data.")
        print(e)

    return render_template("sites/pokonsumen/addForm.html")

@app.route('/pokonsumen/info/<int:id>', methods=['GET'])
def pokonsumenInfo(id):
    pokonsumen = QuotationDetail.query\
        .join(QuotationDB, QuotationDetail.quotation_id==QuotationDB.id)\
        .join(PODB, PODB.quotation_id==QuotationDB.id)\
        .filter_by(id=id)\
        .join(KonsumenDB, QuotationDB.konsumen_id==KonsumenDB.id)\
        .join(SparepartDB, QuotationDetail.sparepart_number==SparepartDB.id)\
        .join(SparepartName, SparepartDB.sparepart_name==SparepartName.id)\
        .join(SparepartBrand, SparepartDB.sparepart_brand==SparepartBrand.id)\
        .add_columns(\
            PODB.po_number,\
            PODB.po_date,\
            QuotationDB.id,\
            QuotationDB.quotation_date,\
            QuotationDB.quotation_number,\
            QuotationDB.quotation_price,\
            QuotationDB.quotation_ppn,\
            QuotationDB.quotation_materai,\
            QuotationDB.quotation_totalprice,\
            QuotationDB.quotation_validity,\
            SparepartDB.sparepart_number,\
            SparepartName.sparepart_name,\
            QuotationDetail.sparepart_qty,\
            QuotationDetail.sparepart_price,\
            QuotationDetail.sparepart_totalprice,\
            QuotationDB.quotation_number,\
            KonsumenDB.konsumen_address,\
            KonsumenDB.konsumen_name\
        )\
        .all()
    print(quotation)
    return render_template("sites/pokonsumen/info.html", pokonsumen=pokonsumen)


@app.route('/pokonsumen/edit/<int:id>')
def poKonsumenEditForm(id):
    pokonsumen = PODB.query.filter_by(id=id).first()
    listQuotation = QuotationDB.query.all()
    listSparepart = SparepartDB.query.all()
    return render_template("sites/pokonsumen/editForm.html", data=pokonsumen, listQuotation=enumerate(listQuotation), listSparepart=enumerate(listSparepart))

@app.route('/pokonsumen/edit', methods=['POST'])
def poKonsumenEdit():
    if request.method == 'POST':
        id = request.form['id']
        dateNow = datetime.datetime.now()
        po_date = dateNow
        quotation_id = request.form['quotation']
        seller_name = request.form['seller_name']
        po_number = request.form['po_number']
        try:
            pokonsumen = PODB.query.filter_by(id=id).first()
            pokonsumen.po_date=po_date
            pokonsumen.quotation_id=quotation_id
            pokonsumen.seller_name=seller_name
            pokonsumen.po_number=po_number
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/pokonsumen")

@app.route('/pokonsumen/delete/<int:id>')
def poKonsumenDelete(id):
    try:
        pokonsumen = PODB.query.filter_by(id=id).first()
        db.session.delete(pokonsumen)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/pokonsumen")



# DO
@app.route('/do', methods=['GET'])
def do():
    listDO = DODB.query\
        .join(PODB, DODB.po_id==PODB.id)\
        .join(QuotationDB, PODB.quotation_id==QuotationDB.id)\
        .join(KonsumenDB, QuotationDB.konsumen_id==KonsumenDB.id)\
        .add_columns(\
            DODB.id\
            ,DODB.do_date\
            ,DODB.do_number\
            ,KonsumenDB.konsumen_name\
        )
    print(listDO)
    return render_template("sites/do/index.html", listDO=enumerate(listDO))

@app.route('/do/add', methods=['GET'])
def doAddForm():
    listSparepart = SparepartDB.query.all()
    listKonsumen = KonsumenDB.query.all()
    return render_template("sites/do/addForm.html", listSparepart=listSparepart, listKonsumen=enumerate(listKonsumen))

@app.route('/do/add', methods=['POST'])
def doAdd():
    dateNow = datetime.datetime.now()
    do_date = dateNow
    do_number = 'DO.TBJ-' + str(random.randint(1000, 9999))
    po_id = request.form['po_id']
    do_terms = request.form['do_terms']
    
    do_price = request.form['sum_price']
    do_ppn = request.form['ppn']
    do_materai = request.form['materai']
    do_totalprice = request.form['grandprice']

    formCount = request.form['formCount']
    idParent = ""

    try:
        do = DODB(po_id=po_id,
                    do_number=do_number,
                    do_date=do_date,
                    do_price=do_price,
                    do_ppn=do_ppn,
                    do_materai=do_materai,
                    do_totalprice=do_totalprice,
                    do_terms=do_terms)
        db.session.add(do)
        db.session.commit()
        db.session.flush()  
        idParent = do.id
        
    except Exception as e:
        print("Failed to add data.")
        print(e)

    i = 0
    while i < int(formCount):
        i = i + 1
        if 'sparepart_'+ str(i) in request.form:
            do_id = idParent
            sparepart_number = request.form['sparepart_'+ str(i)]
            sparepart_qty = request.form['qty_'+ str(i)]
            sparepart_price = request.form['price_'+ str(i)]
            sparepart_totalprice = request.form['total_price_'+ str(i)]
            try:
                DODet = DODetail(do_id=do_id,
                                    sparepart_number=sparepart_number,
                                    sparepart_qty=sparepart_qty,
                                    sparepart_price=sparepart_price,
                                    sparepart_totalprice=sparepart_totalprice)
                db.session.add(DODet)
                db.session.commit()
            except Exception as e:
                print("Failed to add data.")
                print(e)

    return render_template("sites/do/addForm.html")

@app.route('/do/info/<int:id>', methods=['GET'])
def doInfo(id):
    do = DODetail.query\
        .join(DODB, DODB.id==DODetail.do_id)\
        .filter_by(id=id)\
        .join(SparepartDB, DODetail.sparepart_number==SparepartDB.id)\
        .join(SparepartName, SparepartDB.sparepart_name==SparepartName.id)\
        .join(SparepartBrand, SparepartDB.sparepart_brand==SparepartBrand.id)\
        .add_columns(\
            DODB.id,\
            DODB.do_date,\
            DODB.do_number,\
            DODB.do_terms,\
            DODB.do_price,\
            DODB.do_ppn,\
            DODB.do_materai,\
            DODB.do_totalprice,\
            SparepartDB.sparepart_number,\
            SparepartName.sparepart_name,\
            DODetail.sparepart_qty,\
            DODetail.sparepart_price,\
            DODetail.sparepart_totalprice,\
        )\
        .all()
    print(do)
    return render_template("sites/do/info.html", do=do)

@app.route('/do/edit/<int:id>')
def doEditForm(id):
    do = DODB.query.filter_by(id=id).first()
    listQuotation = QuotationDB.query.all()
    listPo = PODB.query.all()
    return render_template("sites/do/editForm.html", data=do, listQuotation=enumerate(listQuotation), listPo=enumerate(listPo))

@app.route('/do/edit', methods=['POST'])
def doEdit():
    if request.method == 'POST':
        id = request.form['id']
        dateNow = datetime.datetime.now()
        po_date = dateNow
        quotation_id = request.form['quotation']
        seller_name = request.form['seller_name']
        po_number = request.form['po_number']
        try:
            pokonsumen = PODB.query.filter_by(id=id).first()
            pokonsumen.po_date=po_date
            pokonsumen.quotation_id=quotation_id
            pokonsumen.seller_name=seller_name
            pokonsumen.po_number=po_number
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/do")

@app.route('/do/delete/<int:id>')
def doDelete(id):
    try:
        do = DODB.query.filter_by(id=id).first()
        db.session.delete(do)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/do")

# Invoice
@app.route('/invoice', methods=['GET'])
def invoice():
    listInvoice = InvoiceDB.query\
        .join(DODB, InvoiceDB.do_id==DODB.id)\
        .join(PODB, DODB.po_id==PODB.id)\
        .join(QuotationDB, PODB.quotation_id==QuotationDB.id)\
        .join(KonsumenDB, QuotationDB.konsumen_id==KonsumenDB.id)\
        .add_columns(\
            InvoiceDB.id\
            ,DODB.do_date\
            ,InvoiceDB.invoice_number\
            ,KonsumenDB.konsumen_name\
        )
    print(listInvoice)
    return render_template("sites/invoice/index.html", listInvoice=enumerate(listInvoice))

@app.route('/invoice/add', methods=['GET'])
def invoiceAddForm():
    return render_template("sites/invoice/addForm.html")

@app.route('/invoice/add', methods=['POST'])
def invoiceAdd():
    dateNow = datetime.datetime.now()
    invoice_date = dateNow
    invoice_number = 'INV.TBJ-' + str(random.randint(1000, 9999))
    do_id = request.form['do_id']
    invoice_terms = request.form['invoice_terms']

    try:
        invoice = InvoiceDB(do_id=do_id,
                    invoice_number=invoice_number,
                    invoice_date=invoice_date,
                    invoice_terms=invoice_terms)
        db.session.add(invoice)
        db.session.commit()
        
    except Exception as e:
        print("Failed to add data.")
        print(e)

    return render_template("sites/invoice/addForm.html")

@app.route('/invoice/edit/<int:id>')
def invoiceEditForm(id):
    invoice = InvoiceDB.query.filter_by(id=id).first()
    listDo = DODB.query.all()
    print(invoice)
    return render_template("sites/invoice/editForm.html", data=invoice, listDo=enumerate(listDo))

@app.route('/invoice/edit', methods=['POST'])
def invoiceEdit():
    if request.method == 'POST':
        id = request.form['id']
        dateNow = datetime.datetime.now()
        invoice_date = dateNow
        do_id = request.form['do_id']
        invoice_terms = request.form['invoice_terms']
        try:
            invoice = InvoiceDB.query.filter_by(id=id).first()
            invoice.invoice_date=invoice_date
            invoice.do_id=do_id
            invoice.invoice_terms=invoice_terms
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/invoice")

@app.route('/invoice/delete/<int:id>')
def invoiceDelete(id):
    try:
        invoice = InvoiceDB.query.filter_by(id=id).first()
        db.session.delete(invoice)
        db.session.commit()
    except Exception as e:
        print("Failed to delete data")
        print(e)
    return redirect("/invoice")

@app.route('/invoice/info/<int:id>', methods=['GET'])
def invoiceInfo(id):
    invoice = DODetail.query\
        .join(DODB, DODB.id==DODetail.do_id)\
        .join(InvoiceDB, InvoiceDB.do_id==DODB.id)\
        .filter_by(id=id)\
        .join(SparepartDB, DODetail.sparepart_number==SparepartDB.id)\
        .join(SparepartName, SparepartDB.sparepart_name==SparepartName.id)\
        .join(SparepartBrand, SparepartDB.sparepart_brand==SparepartBrand.id)\
        .add_columns(\
            DODB.id,\
            DODB.do_date,\
            DODB.do_number,\
            DODB.do_terms,\
            DODB.do_price,\
            DODB.do_ppn,\
            DODB.do_materai,\
            DODB.do_totalprice,\
            SparepartDB.sparepart_number,\
            SparepartName.sparepart_name,\
            DODetail.sparepart_qty,\
            DODetail.sparepart_price,\
            DODetail.sparepart_totalprice,\
        )\
        .all()
    print(invoice)
    return render_template("sites/invoice/info.html", invoice=invoice)

# Master json
@app.route('/master/konsumen', methods=['GET'])
def konsumenMaster():
    konsumen = KonsumenDB.query.all()
    return json.dumps(KonsumenDB.serialize_list(konsumen))

@app.route('/master/sparepart', methods=['GET'])
def sparepartlMaster():
    s = text("\
        SELECT \
        *\
        ,spr.id as spid\
        FROM sparepartDB as spr \
        INNER JOIN sparepart_name as name ON name.id = spr.sparepart_name\
        INNER JOIN sparepart_brand as brand ON brand.id = spr.sparepart_brand\
    ")
    quotationdetail = db.engine.execute(s).fetchall() 
    return json.dumps([dict(r) for r in quotationdetail], default=alchemyencoder)

@app.route('/master/quotation/<string:validity>', methods=['GET'])
def quotationMaster(validity):
    validityVal = validity
    s = text("\
        SELECT \
        * \
        FROM quotationDB as quo \
        WHERE quotation_validity = 1\
    ")
    quotation = db.engine.execute(s, x=validityVal).fetchall() 
    return json.dumps([dict(r) for r in quotation], default=alchemyencoder)

@app.route('/master/quotationdetail/<string:quotation_id>', methods=['GET'])
def quotationdetailMaster(quotation_id):
    s = text("\
        SELECT \
        *\
        ,sparepart.id as spid\
        FROM quotation_detail as quodet \
        INNER JOIN quotationDB as quo ON quodet.quotation_id = quo.id\
        INNER JOIN sparepartDB as sparepart ON quodet.sparepart_number = sparepart.id\
        INNER JOIN sparepart_name as sparepartname ON sparepart.sparepart_name = sparepartname.id\
        WHERE quodet.quotation_id = :x \
    ")
    quotationdetail = db.engine.execute(s, x=quotation_id).fetchall() 
    return json.dumps([dict(r) for r in quotationdetail], default=alchemyencoder)

@app.route('/master/po', methods=['GET'])
def poMaster():
    s = text("\
        SELECT \
        *\
        ,po.id AS poid \
        FROM PODB AS po \
        INNER JOIN quotationDB AS quo ON po.quotation_id = quo.id \
        INNER JOIN konsumenDB AS kon ON quo.konsumen_id = kon.id \
    ")
    podb = db.engine.execute(s).fetchall() 
    return json.dumps([dict(r) for r in podb], default=alchemyencoder)

@app.route('/master/supplier', methods=['GET'])
def supplierMaster():
    supplier = SupplierDB.query.all()
    return json.dumps(SupplierDB.serialize_list(supplier))
@app.route('/master/do', methods=['GET'])
def doMaster():
    s = text("\
        SELECT \
        *\
        ,do.id as doid\
        FROM DODB AS do \
        INNER JOIN PODB AS po ON do.po_id = po.id \
        INNER JOIN quotationDB AS quo ON po.quotation_id = quo.id \
        INNER JOIN konsumenDB AS kon ON quo.konsumen_id = kon.id \
    ")
    dodb = db.engine.execute(s).fetchall() 
    return json.dumps([dict(r) for r in dodb], default=alchemyencoder)

@app.route('/master/dodetail/<string:do_id>', methods=['GET'])
def dodetailMaster(do_id):
    s = text("\
        SELECT \
        *\
        ,sparepart.id as spid\
        FROM do_detail as dodet \
        INNER JOIN sparepartDB as sparepart ON dodet.sparepart_number = sparepart.id\
        INNER JOIN sparepart_name as sparepartname ON sparepart.sparepart_name = sparepartname.id\
        WHERE dodet.do_id = :x \
    ")
    dodetail = db.engine.execute(s, x=do_id).fetchall() 
    return json.dumps([dict(r) for r in dodetail], default=alchemyencoder)

@app.route('/master/invoice/<string:invoice_id>', methods=['GET'])
def invoiceMaster(invoice_id):
    s = text("\
        SELECT \
        *\
        ,sparepart.id as sparepart_id\
        FROM do_detail as dodet \
        INNER JOIN sparepartDB as sparepart ON dodet.sparepart_number = sparepart.id\
        INNER JOIN invoiceDB as inv ON inv.do_id = dodet.do_id\
        INNER JOIN sparepart_name as sparepartname ON sparepart.sparepart_name = sparepartname.id\
        WHERE inv.id = :x \
    ")
    invoiceDetail = db.engine.execute(s, x=invoice_id).fetchall() 
    return json.dumps([dict(r) for r in invoiceDetail], default=alchemyencoder)

dirname = os.path.dirname(__file__)

# generate pdf
def generatePDF(filename,variant,data):
    if variant == 'po':
        templ = 'pdf/po.html'
    elif variant == 'do':
        templ = 'pdf/do.html'
    elif variant == 'invoice':
        templ = 'pdf/invoice.html'
    elif variant == 'quotation':
        templ = 'pdf/quotation.html'
        
    # Make a PDF straight from HTML in a string.
    html = render_template(templ, name=data)

    pdf = HTML(string=html).write_pdf()

    if os.path.exists(dirname):

        f = open(os.path.join(dirname, '../file/'+ variant +'/'+ filename +'.pdf'), 'wb')
        f.write(pdf)
    
    return 'success'

@app.route('/setdoc/<string:filename>', methods=['GET'])
def setdoc(filename):
    return render_template("pdf/"+ filename +".html")