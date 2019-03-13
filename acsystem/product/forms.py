from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Length, Optional
from acsystem.models import Productcategory, Unit, Product
from flask_login import current_user


class ProductCategoryForm(FlaskForm):
    name = StringField('Product Category Name', validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_name(self, name):
        productcategories = Productcategory.query.filter_by(company_id = current_user.activecompany).all()
        for category in productcategories:
            if category.name == name.data:
                flash(f"Category already exist with this name!","warning")
                raise ValidationError("Category already exist!")


class UnitForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(), Length(min=1, max=40)])
    name = StringField('Unit Name', validators=[Optional()])
    submit = SubmitField('Save')

    def validate_symbol(self, symbol):
        units = Unit.query.filter_by(company_id = current_user.activecompany).all()
        for unit in units:
            if unit.symbol == symbol.data:
                flash(f"Symbol already exist with this name!","warning")
                raise ValidationError("Symbol already exist!")


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    category = SelectField("Product Category", choices=[("","Select Category"),("Primary","Primary")], validators=[DataRequired()])
    unit = SelectField("Unit", choices=[("","Select Unit")])
    quantity = IntegerField("Quantity", validators=[Optional()])
    rate = IntegerField("Rate", validators=[Optional()])
    salesprice = IntegerField("Sales Price", validators=[Optional()])
    submit = SubmitField('Save')

    def validate_name(self, name):
        products = Product.query.filter_by(company_id = current_user.activecompany).all()
        for product in products:
            if product.name == name.data:
                flash(f"Name already exist with this name!","warning")
                raise ValidationError("Name already exist!")


class ProductUpdateForm(FlaskForm):
    vdname = StringField('Product Name', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    category = SelectField("Product Category", choices=[("","Select Category"),("Primary","Primary")], validators=[DataRequired()])
    unit = SelectField("Unit", choices=[("","Select Unit")])
    quantity = IntegerField("Quantity", validators=[Optional()])
    rate = IntegerField("Rate", validators=[Optional()])
    salesprice = IntegerField("Sales Price", validators=[Optional()])
    submit = SubmitField('Save')

    def validate_name(self, name):
        if self.vdname.data != name.data:  
            print(self.vdname.data)  
            print(name.data)
            products = Product.query.filter_by(company_id = current_user.activecompany).all()
            for product in products:
                if product.name == name.data:
                    flash(f"Name already exist with this name!","warning")
                    raise ValidationError("Name already exist!")