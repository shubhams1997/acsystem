from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from acsystem.models import FixedGroup, Group
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
                raise ValidationError("Group already exist!")
        if fixedgroup:
            raise ValidationError("Group already exist!")


