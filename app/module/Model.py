from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

# SupplierDB, SparepartDetail, SparepartDB, QuotationDB, QuotationDetail, KonsumenDB, DODB, PODB, PODetail

class SupplierDB(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    supplier_name = db.Column(db.String(255), nullable=False)
    supplier_alamat = db.Column(db.String(255), nullable=False)
    supplier_phone = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class SparepartDetail(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    supplier_name = db.Column(db.String(255), nullable=False)
    sparepart_number = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class SparepartDB(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    sparepart_name = db.Column(db.String(255), nullable=False)
    sparepart_number = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class QuotationDB(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    quotation_date = db.Column(db.DateTime, nullable=False)
    konsumen_id = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class QuotationDetail(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    quotation_number = db.Column(db.Integer, nullable=False)
    sparepart_number = db.Column(db.Integer, nullable=False)
    sparepart_qty = db.Column(db.Integer, nullable=False)
    sparepart_price = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class KonsumenDB(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    konsumen_id = db.Column(db.Integer, nullable=False)
    konsumen_name = db.Column(db.String(255), nullable=False)
    konsumen_address = db.Column(db.String(255), nullable=False)
    konsumen_phone = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class DODB(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    do_number = db.Column(db.Integer, nullable=False)
    do_date = db.Column(db.DateTime, nullable=False)
    sparepart_name = db.Column(db.String(255), nullable=False)
    sparepart_number = db.Column(db.Integer, nullable=False)
    sparepart_qty = db.Column(db.Integer, nullable=False)
    sparepart_brand = db.Column(db.String(255), nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)
    sender_name = db.Column(db.String(255), nullable=False)
    receiver_nama = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class PODB(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    po_date = db.Column(db.DateTime, nullable=False)
    seller_nama = db.Column(db.String(255), nullable=False)
    konsumen_name = db.Column(db.String(255), nullable=False)
    po_number = db.Column(db.Integer, nullable=False)
    po_reference_number = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class PODetail(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    po_date = db.Column(db.DateTime, nullable=False)
    sparepart_name = db.Column(db.String(255), nullable=False)
    sparepart_qty = db.Column(db.Integer, nullable=False)
    konsumen_id = db.Column(db.Integer, nullable=False)
    sparepart_price = db.Column(db.Integer, nullable=False)
    sparepart_brand = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)
