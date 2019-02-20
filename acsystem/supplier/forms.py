from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextField
from wtforms.validators import DataRequired, Length, Optional, Email

class SupplierForm(FlaskForm):
    name = StringField('Customer Name', validators=[DataRequired(), Length(min=3, max=40)])
    first = StringField('First Name', validators=[Optional(), Length(min=3, max=40)])
    last = StringField('Last Name', validators=[Optional(), Length(min=3, max=40)])
    mailingname = StringField('Mailing Name', validators=[Length(min=3, max=40), DataRequired()])
    address = StringField('Address', validators=[Length(min=5, max=100), Optional()])
    country = SelectField('Country',choices=[("","Select Country")], validators=[Optional()])
    state = StringField('State', validators=[Optional()])
    pin = IntegerField('ZIP', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = IntegerField('Phone', validators=[Length(min=10, max=13), Optional()])
    gstno = IntegerField('GST NO', validators=[Optional()])
    openingbalance = IntegerField('Opening Balance', validators=[Optional()])
    description = TextField('Description')
    submit = SubmitField('Save')

