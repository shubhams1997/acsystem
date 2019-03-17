from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class SalesForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    customer = SelectField('Customer', choices=[("","Select Customer")])
    submit = SubmitField('Save')

class SalesItemForm(FlaskForm):
    product = SelectField('Product', choices=[("","Select Product")])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    rate = IntegerField("Rate", validators=[DataRequired()])
    submit = SubmitField("Save")

