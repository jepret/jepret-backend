import os
import hashlib
import peewee as pw
from datetime import datetime
from playhouse.shortcuts import model_to_dict


db = pw.MySQLDatabase(
    os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
)


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.now)
    updated_at = pw.DateTimeField(default=datetime.now)

    def save(self, force_insert=False, only=None):
        self.updated_at = datetime.now()
        super(BaseModel, self).save(force_insert, only)

    def to_dict(self, exclude=[]):
        return model_to_dict(self, recurse=False, backrefs=False, exclude=exclude)

    class Meta:
        database = db


class User(BaseModel):
    name = pw.CharField()
    email = pw.CharField(default="")
    id_card = pw.CharField(unique=True)
    phone_number = pw.CharField(unique=True)
    password = pw.CharField()

    @staticmethod
    def hash(password):
        result = hashlib.md5(password.encode())
        return result.hexdigest()

    def save(self, *args, **kwargs):
        self.password = self.hash(self.password)
        super().save(*args, **kwargs)

    def to_dict(self, exclude=[]):
        exclude.append(User.password)
        return super().to_dict(exclude=exclude)


class UMKM(BaseModel):
    owner = pw.ForeignKeyField(User, backref="umkms")
    name = pw.CharField()
    lat = pw.FloatField(default=0.0)
    lng = pw.FloatField(default=0.0)
    sector = pw.CharField()
    address = pw.CharField()
    city = pw.CharField()
    province = pw.CharField()
    founding_date = pw.DateField()


class Verification(BaseModel):
    verifier = pw.ForeignKeyField(User, backref="verifications")
    umkm = pw.ForeignKeyField(UMKM, backref="verifications")
    photo = pw.CharField()
    star = pw.IntegerField(default=0)
    review = pw.CharField(default="")
