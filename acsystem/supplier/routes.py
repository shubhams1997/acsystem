from flask import Blueprint, render_template, url_for, current_app, flash, redirect, abort, request
from flask_login import login_required, current_user
from acsystem import db
from acsystem.models import Supplier, Countries
from acsystem.supplier.forms import SupplierForm

suppliers = Blueprint('suppliers', __name__)

@suppliers.route('/supplier')
@login_required
def supplierlist():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    suppliers = Supplier.query.filter_by(company_id = current_user.activecompany).all()
    return render_template('suppliertemplate/supplierlist.html', title='suppliers', suppliers=suppliers)


@suppliers.route("/supplier/addsupplier", methods=['GET','POST'])
@login_required
def addsupplier():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    form = SupplierForm()
    form.country.choices+= [(str(country.name), country.name) for country in Countries.query.all()]
    if form.validate_on_submit():
        supplier = Supplier(name = form.name.data, first= form.first.data, last = form.last.data
                    , mailingname = form.mailingname.data
                    , address = form.address.data, country = form.country.data, state = form.state.data
                    , pin = form.pin.data, email = form.email.data, phoneno = form.phone.data
                    , gstno = form.gstno.data, description = form.description.data, company_id = current_user.activecompany)
        db.session.add(supplier)
        db.session.commit()
        flash(f"Supplier Created Succefully!","success")
        return redirect(url_for('suppliers.supplierlist'))
    return render_template("suppliertemplate/addsupplier.html", title="Add Supplier", form=form)


@suppliers.route('/supplier/details/<int:supplier_id>', methods=['GET','POST'])
@login_required
def showsupplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    if supplier.company_id != current_user.activecompany:
        abort(403)
    return render_template('suppliertemplate/supplierdetail.html', title=supplier.name, supplier = supplier)


@suppliers.route('/supplier/<int:supplier_id>/deletesupplier', methods=["POST"])
@login_required
def deletesupplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    if supplier.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(supplier)
    db.session.commit()
    flash(f"Supplier {supplier.name} deleted Successfully","success")
    return redirect(url_for('suppliers.supplierlist'))


@suppliers.route('/supplier/details/<int:supplier_id>/update', methods=['GET','POST'])
@login_required
def updatesupplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    if supplier.company_id != current_user.activecompany:
        abort(403)
    form = SupplierForm()
    form.country.choices+= [(str(country.name), country.name) for country in Countries.query.all()]
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.mailingname = form.mailingname.data
        supplier.first = form.first.data
        supplier.last = form.last.data
        supplier.address = form.address.data
        supplier.country = form.country.data
        supplier.state = form.state.data
        supplier.pin = form.pin.data
        supplier.email = form.email.data
        supplier.phoneno = form.phone.data 
        supplier.gstno = form.gstno.data
        supplier.description = form.description.data
        db.session.commit()
        flash(f'Your supplier details has been Updated!', 'success')
        return redirect(url_for('suppliers.showsupplier', supplier_id = supplier_id))
    elif request.method == 'GET':
        form.name.data = supplier.name 
        form.mailingname.data = supplier.mailingname 
        form.first.data = supplier.first
        form.last.data = supplier.last
        form.address.data = supplier.address 
        form.country.data = supplier.country 
        form.state.data = supplier.state 
        form.pin.data = supplier.pin 
        form.email.data = supplier.email 
        form.phone.data  = supplier.phoneno 
        form.gstno.data = supplier.gstno 
        form.description.data = supplier.description
    return render_template('suppliertemplate/updatesupplier.html', title=supplier.name, form=form) 
