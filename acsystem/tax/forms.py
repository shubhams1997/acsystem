from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from acsystem.models import Tax
from flask_login import current_user

class TaxForm(FlaskForm):
    name = StringField("Tax Name", validators=[DataRequired(), Length(min=5, max=50)])
    percentage = IntegerField("Percentage (Only Numerical values)", validators=[DataRequired()])
    submit = SubmitField("Add Tax")

    def validate_name(self, name):
        taxes = Tax.query.filter_by(company_id = current_user.activecompany).all()
        for tax in taxes:
            if tax.name == name.data:
                raise ValidationError("Tax with this name Already Exist!")
