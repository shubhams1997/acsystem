from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextField
from wtforms.validators import DataRequired, Email, Length, URL, ValidationError, Optional
from acsystem.models import Company
from wtforms.fields.html5 import DateField
from flask_login import current_user


class CompanyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=40)])
    mailingname = StringField('Mailing Name', validators=[DataRequired(), Length(min=3, max=40)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=100)])
    country = SelectField('Country', choices=[("","Select Country")], validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pin = IntegerField('ZIP', validators=[Optional()])
    phone = IntegerField('Phone', validators=[Optional()])
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
    country = SelectField('Country', choices=[("","Select Country")], validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pin = IntegerField('ZIP', validators=[Optional()])
    phone = IntegerField('Phone', validators=[Optional()])
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

