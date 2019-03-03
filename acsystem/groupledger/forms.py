from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Length
from acsystem.models import FixedGroup, Group, Ledger
from flask_login import current_user


class GroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    under = SelectField('Under', choices=[("Assets","Assets"),("liability","Liability"),("Income","Income"),("Expense","Expense")])
    submit = SubmitField('Save')

    def validate_name(self, name):
        fixedgroup = FixedGroup.query.filter_by(name = name.data).first()
        grouplist = Group.query.filter_by(company_id = current_user.activecompany).all()
        for group in grouplist:
            if group.name == name.data:
                flash(f"Group already exist with this name!","warning")
                raise ValidationError("Group already exist!")
        if fixedgroup:
            flash(f"Group already exist with this name!","warning")
            raise ValidationError("Group already exist!")


class LedgerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=40)])
    under = SelectField("Under", choices=[("","Select Group")], validators=[DataRequired()])
    affectinventory = BooleanField("Affect Inventory")
    submit = SubmitField('Save')

    def validate_name(self, name):
        ledgers = Ledger.query.filter_by(company_id = current_user.activecompany).all()
        for ledger in ledgers:
            if ledger.name == name.data:
                flash(f"Ledger already exist with this name!","warning")
                raise ValidationError("Ledger already exist with this name!")
