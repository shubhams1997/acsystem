from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextField
from wtforms.validators import DataRequired, Length, Optional, Email, ValidationError
from acsystem.models import Customer
from flask_login import current_user

class CustomerForm(FlaskForm):
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
    gstno = StringField('GST NO', validators=[Optional()])
    openingbalance = IntegerField('Opening Balance', validators=[Optional()])
    description = TextField('Description')
    submit = SubmitField('Save')

    def validate_name(self, name):
        customers = Customer.query.filter_by(company_id = current_user.activecompany).all()
        for customer in customers:
            if customer.name == name.data:
                raise ValidationError("Customer already Exist with this name.")

class CustomerUpdateForm(FlaskForm):
    vdname = StringField('Product Name', validators=[DataRequired()])
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
    gstno = StringField('GST NO', validators=[Optional()])
    openingbalance = IntegerField('Opening Balance', validators=[Optional()])
    description = TextField('Description')
    submit = SubmitField('Save')

    def validate_name(self, name):
        if self.vdname.data != name.data:  
            print(self.vdname.data)  
            print(name.data)
            customers = Customer.query.filter_by(company_id = current_user.activecompany).all()
            for customer in customers:
                if customer.name == name.data:
                    flash(f"Customer already exist with this name!","warning")
                    raise ValidationError("Name already exist!")


