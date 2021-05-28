from flask_sqlalchemy import SQLAlchemy
from app import app
from sqlalchemy.inspection import inspect

db = SQLAlchemy(app)

# SupplierDB, SparepartDetail, SparepartDB, QuotationDB, QuotationDetail, KonsumenDB, DODB, PODB, PODetail

class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    def serialize_list(l):
        return [m.serialize() for m in l]

class SupplierDB(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    supplier_name = db.Column(db.String(255), nullable=False)
    supplier_alamat = db.Column(db.String(255), nullable=False)
    supplier_phone = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class SparepartName(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    sparepart_name = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class SparepartBrand(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    sparepart_brand = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class SparepartDB(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    sparepart_name = db.Column(db.String(255), nullable=False)
    sparepart_number = db.Column(db.String(255), nullable=False)
    sparepart_brand = db.Column(db.String(255), nullable=False)
    sparepart_price = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class QuotationDB(db.Model,Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    quotation_date = db.Column(db.DateTime, nullable=False)
    quotation_number = db.Column(db.String(255), nullable=False)
    quotation_validity = db.Column(db.Integer, nullable=False)
    konsumen_id = db.Column(db.Integer, nullable=False)
    quotation_price = db.Column(db.Integer, nullable=False)
    quotation_ppn = db.Column(db.Integer, nullable=False)
    quotation_materai = db.Column(db.Integer, nullable=False)
    quotation_totalprice = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class QuotationDetail(db.Model,Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    quotation_id = db.Column(db.String(255), nullable=False)
    sparepart_number = db.Column(db.String(255), nullable=False)
    sparepart_qty = db.Column(db.Integer, nullable=False)
    sparepart_price = db.Column(db.Integer, nullable=False)
    sparepart_totalprice = db.Column(db.Integer, nullable=False)
    sparepart_description = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class KonsumenDB(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    konsumen_id = db.Column(db.Integer, nullable=False)
    konsumen_name = db.Column(db.String(255), nullable=False)
    konsumen_address = db.Column(db.String(255), nullable=False)
    konsumen_phone = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class DODB(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    do_number = db.Column(db.Integer, nullable=False)
    po_id = db.Column(db.String(255), nullable=False)
    do_date = db.Column(db.DateTime, nullable=False)
    po_id = db.Column(db.String(255), nullable=False)
    do_number = db.Column(db.String(255), nullable=False)
    do_terms = db.Column(db.String(255), nullable=True)
    do_price = db.Column(db.Integer, nullable=False)
    do_ppn = db.Column(db.Integer, nullable=False)
    do_materai = db.Column(db.Integer, nullable=False)
    do_totalprice = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class DODetail(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    do_id = db.Column(db.String(255), nullable=False)
    sparepart_number = db.Column(db.String(255), nullable=False)
    sparepart_qty = db.Column(db.Integer, nullable=False)
    sparepart_price = db.Column(db.Integer, nullable=False)
    sparepart_totalprice = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class InvoiceDB(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    do_id = db.Column(db.String(255), nullable=False)
    invoice_date = db.Column(db.DateTime, nullable=False)
    invoice_number = db.Column(db.String(255), nullable=False)
    invoice_terms = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class PODB(db.Model,Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    quotation_id = db.Column(db.String(255), nullable=True)
    seller_name = db.Column(db.String(255), nullable=False)
    po_date = db.Column(db.DateTime, nullable=False)
    po_number = db.Column(db.String(255), nullable=False)
    po_validity = db.Column(db.Integer, nullable=False)
    konsumen_id = db.Column(db.Integer, nullable=False)
    po_price = db.Column(db.Integer, nullable=False)
    po_ppn = db.Column(db.Integer, nullable=False)
    po_materai = db.Column(db.Integer, nullable=False)
    po_totalprice = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class PODetail(db.Model,Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    po_id = db.Column(db.String(255), nullable=False)
    sparepart_number = db.Column(db.String(255), nullable=False)
    sparepart_qty = db.Column(db.Integer, nullable=False)
    sparepart_price = db.Column(db.Integer, nullable=False)
    sparepart_totalprice = db.Column(db.Integer, nullable=False)
    sparepart_description = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class POKeluarDB(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    po_id = db.Column(db.String(255), nullable=False)
    supplier_id = db.Column(db.String(255), nullable=False)
    pokeluar_number = db.Column(db.String(255), nullable=False)
    pokeluar_date = db.Column(db.DateTime, nullable=False)
    pokeluar_price = db.Column(db.Integer, nullable=False)
    pokeluar_ppn = db.Column(db.Integer, nullable=False)
    pokeluar_materai = db.Column(db.Integer, nullable=False)
    pokeluar_totalprice = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class POKeluarDetail(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    pokeluar_id = db.Column(db.String(255), nullable=False)
    sparepart_number = db.Column(db.String(255), nullable=False)
    sparepart_qty = db.Column(db.Integer, nullable=False)
    sparepart_price = db.Column(db.Integer, nullable=False)
    sparepart_totalprice = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class InvoiceSupplierDB(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    pokeluar_id = db.Column(db.String(255), nullable=False)
    invoiceSupplier_number = db.Column(db.String(255), nullable=False)
    invoiceSupplier_date = db.Column(db.DateTime, nullable=False)
    invoiceSupplier_price = db.Column(db.Integer, nullable=False)
    invoiceSupplier_ppn = db.Column(db.Integer, nullable=False)
    invoiceSupplier_materai = db.Column(db.Integer, nullable=False)
    invoiceSupplier_totalprice = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)
    

class UserManagementDB(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    user_pass = db.Column(db.String(255), nullable=False)
    user_level = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    created_add = db.Column(db.DateTime, nullable=True)
    updated_add = db.Column(db.DateTime, nullable=True)

class numberCount(db.Model, Serializer):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    channel = db.Column(db.String(255), nullable=False)
    idGrandpa = db.Column(db.String(255), nullable=True)
    idParent = db.Column(db.String(255), nullable=False)
    flag = db.Column(db.String(255), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)