import os
import hashlib
import peewee as pw
from datetime import datetime
from playhouse.shortcuts import model_to_dict
from core.util import generate_random_str

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
        result = model_to_dict(self, recurse=False, backrefs=False, exclude=exclude)
        result['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        result['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return result

    class Meta:
        database = db


class User(BaseModel):
    name = pw.CharField()
    email = pw.CharField(default="")
    id_card = pw.CharField(unique=True)
    phone_number = pw.CharField(unique=True)
    password = pw.CharField()
    balance = pw.IntegerField(default=0)

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
    photo = pw.CharField()
    lat = pw.FloatField(default=0.0)
    lng = pw.FloatField(default=0.0)
    sector = pw.CharField()
    address = pw.CharField()
    city = pw.CharField()
    province = pw.CharField()
    founding_date = pw.DateField()
    balance = pw.IntegerField(default=0)
    unique_id = pw.CharField(default=generate_random_str)

    def to_dict(self, exclude=[], exclude_balance=True):
        if exclude_balance:
            exclude.append(UMKM.balance)

        result = super().to_dict(exclude)
        result['founding_date'] = self.founding_date.strftime("%Y-%m-%d %H:%M:%S")
        return result


class UMKMDetail(BaseModel):
    umkm = pw.ForeignKeyField(UMKM, backref="detail")
    owner_name = pw.CharField()
    position = pw.CharField()
    gender = pw.CharField()
    birth_date = pw.CharField()
    expert_count = pw.IntegerField()
    worker_count = pw.IntegerField()
    gross_revenue = pw.IntegerField()
    average_price = pw.IntegerField()
    operational_cost = pw.IntegerField()
    need_funding = pw.BooleanField()
    funding_amount = pw.IntegerField()
    funding_month_count = pw.IntegerField()
    money_eq_success = pw.IntegerField()
    money_eq_competence = pw.IntegerField()
    do_care_money = pw.IntegerField()


class Campaign(BaseModel):
    umkm = pw.ForeignKeyField(UMKM, backref="campaign")
    active = pw.BooleanField(default=False)
    budget = pw.IntegerField(default=0)
    price = pw.IntegerField(default=0)


class UMKMValidator(BaseModel):
    umkm = pw.ForeignKeyField(UMKM, backref="validator")
    seed_images = pw.CharField(default="[]")


class UMKMStatistic(BaseModel):
    umkm = pw.ForeignKeyField(UMKM, backref="statistic")
    negative_review_count = pw.IntegerField(default=0)
    positive_review_count = pw.IntegerField(default=0)
    neutral_review_count = pw.IntegerField(default=0)


class Verification(BaseModel):
    verifier = pw.ForeignKeyField(User, backref="verifications")
    umkm = pw.ForeignKeyField(UMKM, backref="verifications")
    photo = pw.CharField()
    star = pw.IntegerField(default=0)
    review = pw.CharField(default="")
    pending = pw.BooleanField(default=True)
    success = pw.BooleanField(default=False)
    sentiment = pw.CharField()


class QuestionAnswer(BaseModel):
    verification = pw.ForeignKeyField(Verification, backref="qas")
    question = pw.CharField()
    answer = pw.CharField()


class File(BaseModel):
    owner = pw.ForeignKeyField(User, backref="files")
    filename = pw.CharField()
    unique_id = pw.CharField(default=generate_random_str)


class Transaction(BaseModel):
    sender = pw.ForeignKeyField(User, backref="transactions")
    receiver = pw.ForeignKeyField(UMKM, backref="transactions")
    amount = pw.IntegerField()

    def to_dict(self, exclude=[]):
        result = super().to_dict(exclude)
        result['receiver'] = self.receiver.to_dict()

        return result
