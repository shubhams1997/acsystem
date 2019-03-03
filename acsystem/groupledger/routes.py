from flask import Blueprint, redirect, render_template, flash, request, url_for, abort
from acsystem import db
from acsystem.models import Group, FixedGroup, Ledger
from acsystem.groupledger.forms import GroupForm, LedgerForm
from flask_login import current_user, login_required

groupledgers = Blueprint("groupledgers",__name__)

@groupledgers.route('/groups', methods=['GET','POST'])
@login_required
def group():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    form = GroupForm()
    if form.validate_on_submit():
        usergroup = Group(name = form.name.data, under = form.under.data, company_id=current_user.activecompany)
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

@groupledgers.route('/ledgers', methods=['GET','POST'])
@login_required
def ledger():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    form = LedgerForm()
    form.under.choices+= [(str(fixedgroup.name), fixedgroup.name) for fixedgroup in FixedGroup.query.all()]
    form.under.choices+= [(str(group.name), group.name) for group in Group.query.filter_by(company_id = current_user.activecompany).all()]
    if form.validate_on_submit():
        group = Group.query.filter_by(name = form.under.data).first()
        userledger = Ledger(name = form.name.data, under = group.id, affectinventory = form.affectinventory.data, company_id=current_user.activecompany)
        db.session.add(userledger)
        db.session.commit()
        flash(f"Ledger Added Successfully.","success")
        return redirect(url_for('groupledgers.ledger'))
    ledgers = Ledger.query.filter_by(company_id = current_user.activecompany).all()
    return render_template('groupledger/showledgers.html', title="Ledgers", form=form, ledgers = ledgers )


@groupledgers.route("/ledgers/delete/<int:ledger_id>", methods=['POST'])
@login_required
def deleteledger(ledger_id):
    ledger = Ledger.query.get_or_404(ledger_id);
    if ledger.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(ledger)
    db.session.commit()
    flash(f"Ledger Deleted Successfully.","success")
    return redirect(url_for('groupledgers.ledger'))