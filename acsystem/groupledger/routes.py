from flask import Blueprint, redirect, render_template, flash, request, url_for, abort
from acsystem import db
from acsystem.models import Group, FixedGroup
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
    fixedgroups = FixedGroup.query.all()
    return render_template('groupledger/showgroup.html', title="Groups", form=form, groups = groups, fixedgroups=fixedgroups )


@groupledgers.route("/groups/delete/<int:group_id>", methods=['POST'])
@login_required
def deletegroup(group_id):
    group = Group.query.get_or_404(group_id);
    if group.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(group)
    db.session.commit()
    flash(f"Group Deleted Successfully.","success")
    return redirect(url_for('groupledgers.group'))
