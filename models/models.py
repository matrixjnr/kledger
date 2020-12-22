from config.base import db, ma
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), index=True, nullable=False)
    idnumber = db.Column(db.Integer, index=True, unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    # Relationships
    creditors = relationship("Creditor", backref="user", cascade="all, delete-orphan", lazy='dynamic')
    transactions = relationship("Tx", backref="user", cascade="all, delete-orphan", lazy='dynamic')
    items = relationship("Item", backref="user", cascade="all, delete-orphan", lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.full_name


class Creditor(db.Model):
    __tablename__ = "creditors"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, ForeignKey('users.idnumber'), nullable=False)
    full_name = db.Column(db.String(64), index=True, nullable=False)
    idnumber = db.Column(db.Integer, index=True, unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    debt = db.Column(db.Float, default='0.00')

    # Relationships
    items = relationship("Item", backref="creditor", cascade="all, delete-orphan", lazy='dynamic')
    transactions = relationship("Tx", backref="creditor", cascade="all, delete-orphan", lazy='dynamic')

    def __repr__(self):
        return '<Creditor %r>' % self.full_name


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, ForeignKey('users.idnumber'), nullable=False)
    borrower = db.Column(db.Integer, ForeignKey('creditors.idnumber'), nullable=False)
    item_name = db.Column(db.String(64), index=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)


class Tx(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    creditorid = db.Column(db.Integer, ForeignKey('creditors.id'), nullable=False)
    owner = db.Column(db.Integer, ForeignKey('users.idnumber'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'full_name', 'idnumber', 'phone', 'password')


class CreditorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'owner', 'full_name', 'idnumber', 'phone', 'debt')


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'owner', 'borrower', 'item_name', 'quantity', 'price')


class TxSchema(ma.Schema):
    class Meta:
        fields = ('id', 'creditorid', 'owner', 'amount', 'date')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

creditor_schema = CreditorSchema()
creditors_schema = CreditorSchema(many=True)

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

tx_schema = TxSchema()
txs_schema = TxSchema(many=True)
