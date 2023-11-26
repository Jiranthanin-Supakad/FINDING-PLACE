from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime, timezone , timedelta


class FindBlog(db.Model, SerializerMixin):
    __tablename__ = "find_blog"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    category = db.Column(db.String(50))
    filenameIMG = db.Column(db.String(100))
    idPet = db.Column(db.String(50))
    detail = db.Column(db.String(280))
    subdist = db.Column(db.String(50))
    district = db.Column(db.String(50))
    province = db.Column(db.String(50))
    tel = db.Column(db.String(10))
    date_created = db.Column(DateTime(timezone=True), server_default=func.now())
    date_updated = db.Column(DateTime, default=datetime.utcnow, onupdate=func.now())
    

    def __init__(self, name, email, category, idPet ,subdist, district, province, detail, tel, filenameIMG):
        self.name = name
        self.email = email
        self.category = category
        self.idPet = idPet
        self.subdist = subdist
        self.district = district
        self.province = province
        self.detail = detail
        self.tel = tel
        self.filenameIMG = filenameIMG

    def update(self, name, email, category, idPet ,subdist, district, province, detail, tel, filenameIMG):
        self.name = name
        self.email = email
        self.category = category
        self.idPet = idPet
        self.subdist = subdist
        self.district = district
        self.province = province
        self.detail = detail
        self.tel = tel
        self.filenameIMG = filenameIMG