from flask import Blueprint, redirect, render_template, flash, request, url_for
from acsystem import db
from acsystem.models import Group
from acsystem.groupledger.forms import GroupForm
from flask_login import current_user, login_required

groupledgers = Blueprint("groupledgers",__name__)

@groupledgers.route('/groups', methods=['GET','POST'])
@login_required
def group():
    form = GroupForm()
    if form.validate_on_submit():
        usergroup = Group(name = form.name.data, under = form.under.data, company_id=current_user.activecompany)
        print(usergroup.name)
        db.session.add(usergroup)
        db.session.commit()
        flash(f"Group Added Successfully.","success")
        return redirect(url_for('groupledgers.group'))
    groups = Group.query.filter_by(company_id = current_user.activecompany).all()
    return render_template('groupledger/showgroup.html', title="Groups", form=form, groups = groups )

