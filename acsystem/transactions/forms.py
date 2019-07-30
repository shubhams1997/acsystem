from flask import flash
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SelectField, IntegerField, SubmitField, FormField, FieldList, HiddenField, TextField
from wtforms.fields.html5 import DateField,DateTimeField
from wtforms.validators import DataRequired, ValidationError, Optional
from acsystem.models import Sales, Product
from flask_login import current_user


class SalesItemForm(Form):
    product = SelectField("Product", choices=[("","Select Product")],validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    rate = IntegerField("Rate", validators=[DataRequired()])
    unit = StringField("Unit", validators=[Optional()])

    def validate_quantity(self,quantity):
        prod = Product.query.get_or_404(self.product.data)
        if quantity.data >prod.quantity:
            raise ValidationError("quantity over specified")


class SalesForm(FlaskForm):
    rows = HiddenField("rows")
    date = DateTimeField('Date', validators=[DataRequired()])
    customer = StringField('Customer', validators=[DataRequired()])
    cust_address = StringField('cust_address', validators=[Optional()])
    cust_state = StringField('cust_state', validators=[Optional()])
    cust_country = StringField('cust_country', validators=[Optional()])
    cust_phone = IntegerField('cust_phone', validators=[Optional()])
    invoiceno = IntegerField('Invoice Number', validators=[DataRequired()])
    totalamount = IntegerField("Total", validators=[DataRequired()])
    items = FieldList(FormField(SalesItemForm), min_entries=1)
    description = TextField("Description", validators=[Optional()])
    submit = SubmitField('Save')

    def validate_invoiceno(self, invoiceno):
        allsales = Sales.query.filter_by(company_id = current_user.activecompany).all()
        for sale in allsales:
            if sale.invoiceno == invoiceno.data:
                flash(f"Invoice with this Invoice Number already exist!","warning")
                raise ValidationError('Invoice with this Invoice Number already exist!')
    
    def validate_items(self, items):
        items.min_entries= len(items)
        self.rows.data = len(items)-1
        obj = [{'p':entry.product.data, 'q':entry.quantity.data}for entry in items.entries]
        pro =[]
        qty =[]
        for o in obj:
            if o['p'] in pro:
                qty[pro.index(o['p'])]+=o['q']
            else:
                pro.append(o['p'])
                qty.append(o['q'])
        for i in range(len(pro)):
            prod = Product.query.get(pro[i])
            if prod.quantity < qty[i]:
                flash(f"Same Product saled different time and the combined sailing quantity is greater then available quantity","warning")
                raise ValidationError("Quantity over Specified")      

