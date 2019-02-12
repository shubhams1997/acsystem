from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextField
from wtforms.validators import DataRequired, Email, Length, EqualTo, URL, ValidationError
from acsystem.models import User
from wtforms.fields.html5 import DateField

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
    country = SelectField('Country', choices=[('0','Select'), ("1","india")])
    state = SelectField('State', choices=[('0','Select'), ("2","delhi")])
    pin = StringField('ZIP')
    phone = IntegerField('Phone', validators=[Length(min=9, max=13)])
    email = StringField('Email', validators=[Email()])
    website = StringField('Website', validators=[URL()])
    financialyear = DateField('Financial year')
    booksbegin = DateField('Books Begin From')
    gstno = IntegerField('GST NO')
    description = TextField('Description')
    submit = SubmitField('Create')

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
    submit = SubmitField('Create')
    
    


    
