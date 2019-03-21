from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError    
from acsystem.models import Sales
from flask_login import current_user

class SalesForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    customer = StringField('Customer', validators=[DataRequired()])
    invoiceno = IntegerField('Invoice Number', validators=[DataRequired()])
    totalamount = IntegerField("Total", validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_invoiceno(self, invoiceno):
        allsales = Sales.query.filter_by(company_id = current_user.activecompany).all()
        for sale in allsales:
            if sale.invoiceno == invoiceno.data:
                raise ValidationError('Invoice with this Invoice Number already exist!')

def SIF(arg):
    class SalesItemForm(FlaskForm):
        product = SelectField('Product', choices=[("","Select Product")])
        quantity = IntegerField("Quantity", validators=[DataRequired()])
        rate = IntegerField("Rate", validators=[DataRequired()])
        submititem = SubmitField("Save")
    setattr(SalesItemForm, 'attribute', StringField(arg))
    # setattr(SalesItemForm,'attribute',IntegerField(args))
    return SalesItemForm()

