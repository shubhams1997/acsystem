from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from acsystem.models import User
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

class UpdateUserForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(),Length(min=3, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phoneno = IntegerField("Phone Number", validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Account for this email ID already exist! please choose a different one.')