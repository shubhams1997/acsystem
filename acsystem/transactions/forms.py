from flask_wtf import FlaskForm, Form
from wtforms import StringField, SelectField, IntegerField, SubmitField, FormField, FieldList, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Optional
from acsystem.models import Sales, Product
from flask_login import current_user


class SalesItemForm(Form):
    product = SelectField("", choices=[("","Select Product")],validators=[Optional()])
    quantity = IntegerField("Quantity", validators=[])
    rate = IntegerField("Rate", validators=[])


class SalesForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    customer = StringField('Customer', validators=[DataRequired()])
    invoiceno = IntegerField('Invoice Number', validators=[DataRequired()])
    totalamount = IntegerField("Total")
    items = FieldList(FormField(SalesItemForm), min_entries=2)
    submit = SubmitField('Save')

    def validate_invoiceno(self, invoiceno):
        allsales = Sales.query.filter_by(company_id = current_user.activecompany).all()
        for sale in allsales:
            if sale.invoiceno == invoiceno.data:
                raise ValidationError('Invoice with this Invoice Number already exist!')

