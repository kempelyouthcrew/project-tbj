from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    nim = db.Column(db.String, nullable=False)
    nama = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Nama: {}>".format(self.nama)