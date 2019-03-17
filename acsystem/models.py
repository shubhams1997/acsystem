from acsystem import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first = db.Column(db.String(60), nullable=False)
    last = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique= True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg', nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    companies = db.relationship('Company', backref ='owner', lazy = True, cascade="all, delete-orphan")
    activecompany = db.Column(db.Integer, default=0)
    
    def __init__(self, first, last, email, phone, password):
        self.first = first
        self.last = last
        self.email = email
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f"User('{self.first} {self.activecompany}' )"


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(80), unique=True, nullable=False)
    mailingname = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(40), nullable=False)
    pin = db.Column(db.Integer)
    email = db.Column(db.String(60))
    phoneno = db.Column(db.Integer)
    website = db.Column(db.String(60))
    datecreated = db.Column(db.DateTime, default = datetime.utcnow, nullable=False)
    financialyear = db.Column(db.DateTime, nullable=False)
    booksbegin = db.Column(db.DateTime, nullable=False)
    gstno = db.Column(db.Integer)
    description = db.Column(db.Text)
    customers = db.relationship('Customer', backref='undercompany', lazy=True, cascade="all, delete-orphan")
    suppliers = db.relationship('Supplier', backref='undercompany', lazy=True, cascade="all, delete-orphan")
    groups = db.relationship('Group', backref='undercompany', lazy=True, cascade="all, delete-orphan")
    ledgers = db.relationship('Ledger', backref='undercompany', lazy=True, cascade="all, delete-orphan")
    productcategories = db.relationship('Productcategory', backref='undercompany', lazy=True, cascade="all, delete-orphan")
    products = db.relationship('Product', backref='undercompany', lazy=True, cascade="all, delete-orphan")
    units = db.relationship('Unit', backref='undercompany', lazy=True, cascade="all, delete-orphan")
    sale = db.relationship('Sales', backref='undercompany', lazy=True, cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Company('{self.companyname}', '{self.owner.first}')"


class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    first = db.Column(db.String(40))
    last = db.Column(db.String(40))
    mailingname = db.Column(db.String(40))
    address = db.Column(db.String(100))
    country = db.Column(db.String(30))
    state = db.Column(db.String(30))
    pin = db.Column(db.Integer)
    email = db.Column(db.String(50))
    phoneno = db.Column(db.Integer)
    gstno = db.Column(db.Integer)
    openingbalance = db.Column(db.Integer, default=0, nullable=False)
    currentbalance = db.Column(db.Integer, default=0, nullable=False)
    description = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Customer('{self.name}', '{self.company_id}')"

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    first = db.Column(db.String(40))
    last = db.Column(db.String(40))
    mailingname = db.Column(db.String(40))
    address = db.Column(db.String(100))
    country = db.Column(db.String(30))
    state = db.Column(db.String(30))
    pin = db.Column(db.Integer)
    email = db.Column(db.String(50))
    phoneno = db.Column(db.Integer)
    gstno = db.Column(db.Integer)
    openingbalance = db.Column(db.Integer, default=0, nullable=False)
    currentbalance = db.Column(db.Integer, default=0, nullable=False)
    description = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Supplier('{self.name}', '{self.company_id}')"

class FixedGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    under = db.Column(db.String(20), nullable=False)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    under = db.Column(db.String(20), nullable=False)
    ledgers = db.relationship('Ledger', backref='undergroup', lazy=True, cascade="all, delete-orphan")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Group('{self.name}','{self.under}')"


class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    affectinventory = db.Column(db.Boolean)
    undername = db.Column(db.String(40))
    under = db.Column(db.Integer, db.ForeignKey('group.id', ondelete="CASCADE"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)
    
    def __repr__(self):
        return f"Ledger('{self.name}','{self.under}')"


class Productcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    products = db.relationship('Product', backref='undercategory', lazy=True, cascade="all, delete-orphan")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(40))
    products = db.relationship('Product', backref='underunit', lazy=True, cascade="all, delete-orphan")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('productcategory.id', ondelete="CASCADE"), nullable=False)
    categoryname = db.Column(db.String(40))
    unit = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    unitname = db.Column(db.String(10))
    quantity = db.Column(db.Integer, default=0)
    rate = db.Column(db.Integer)
    salesprice = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(40), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    totalamount = db.Column(db.Integer)
    salesitems = db.relationship('SalesItem', lazy=True, cascade="all, delete-orphan")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)

class SalesItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    undersales = db.Column(db.Integer, db.ForeignKey('sales.id', ondelete="CASCADE"), nullable=False)