from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextField
from wtforms.validators import DataRequired, Email, Length, EqualTo, URL, ValidationError, Optional
from acsystem.models import User, Company
from wtforms.fields.html5 import DateField
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(),Length(min=3, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Account for this email ID already exist! please choose a different one.')

class CompanyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=40)])
    mailingname = StringField('Mailing Name', validators=[DataRequired(), Length(min=3, max=40)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=100)])
    country = SelectField('Country', choices=[], validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pin = StringField('ZIP')
    phone = IntegerField('Phone', validators=[Optional(), Length(min=9, max=13)])
    email = StringField('Email', validators=[Optional(), Email()])
    website = StringField('Website', validators=[Optional(), URL()])
    financialyear = DateField('Financial year', validators=[Optional()])
    booksbegin = DateField('Books Begin From', validators=[Optional()])
    gstno = IntegerField('GST NO', validators=[Optional()])
    description = TextField('Description')
    submit = SubmitField('Save')

    def validate_name(self, name):
        company = Company.query.filter_by(companyname = name.data).first()
        if company:
            raise ValidationError('Company with this Name already exist!')

class UpdateCompanyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=40)])
    mailingname = StringField('Mailing Name', validators=[DataRequired(), Length(min=3, max=40)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=100)])
    country = SelectField('Country', choices=[], validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pin = StringField('ZIP')
    phone = IntegerField('Phone', validators=[Optional(), Length(min=9, max=13)])
    email = StringField('Email', validators=[Optional(), Email()])
    website = StringField('Website', validators=[Optional(), URL()])
    financialyear = DateField('Financial year', validators=[Optional()])
    booksbegin = DateField('Books Begin From', validators=[Optional()])
    gstno = IntegerField('GST NO', validators=[Optional()])
    description = TextField('Description')
    submit = SubmitField('Save')

    def validate_name(self, name):
        activecomp = Company.query.get(current_user.activecompany)
        if name.data != activecomp.companyname:
            company = Company.query.filter_by(companyname = name.data).first()
            if company:
                raise ValidationError('Company with this Name already exist!')

class CustomerForm(FlaskForm):
    name = StringField('Customer Name', validators=[DataRequired(), Length(min=3, max=40)])
    first = StringField('First Name', validators=[Length(min=3, max=40)])
    last = StringField('Last Name', validators=[Length(min=3, max=40)])
    mailingname = StringField('Mailing Name', validators=[Length(min=3, max=40)])
    address = StringField('Address', validators=[Length(min=5, max=100)])
    country = SelectField('Country')
    state = SelectField('State')
    phone = IntegerField('Phone', validators=[Length(min=10, max=13)])
    gstno = IntegerField('GST NO')
    submit = SubmitField('Save')
    
    


    
