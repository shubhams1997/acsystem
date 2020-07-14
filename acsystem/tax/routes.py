from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from acsystem import db
from acsystem.models import Tax
from acsystem.tax.forms import TaxForm

taxes = Blueprint("taxes", __name__)

@taxes.route("/taxes", methods=["GET","POST"])
@login_required
def taxeslist():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    form = TaxForm()
    if form.validate_on_submit():
        newtax = Tax(name = form.name.data, percentage = form.percentage.data, company_id = current_user.activecompany)
        db.session.add(newtax)
        db.session.commit()
        flash(f"New Tax is added Successfully", "success")
        return redirect(url_for('taxes.taxeslist'))
    taxlist = Tax.query.filter_by(company_id = current_user.activecompany).all()
    return render_template("taxtemplate/taxlist.html", title = "Taxes", taxlist = taxlist, form=form)