from flask import Blueprint, render_template, url_for, current_app, flash, redirect, abort, request
from flask_login import login_required, current_user
from acsystem import db
from acsystem.models import Customer, Countries
from acsystem.customer.forms import CustomerForm

customers = Blueprint('customers', __name__)

@customers.route('/customer')
@login_required
def customerlist():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    customers = Customer.query.filter_by(company_id = current_user.activecompany).all()
    return render_template('customertemplate/customerlist.html', title='Customers', customers=customers)


@customers.route("/customer/addcustomer", methods=['GET','POST'])
@login_required
def addcustomer():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    form = CustomerForm()
    form.country.choices+= [(str(country.name), country.name) for country in Countries.query.all()]
    if form.validate_on_submit():
        customer = Customer(name = form.name.data, first= form.first.data, last = form.last.data
                    , mailingname = form.mailingname.data, openingbalance = form.openingbalance.data, currentbalance = form.openingbalance.data
                    , address = form.address.data, country = form.country.data, state = form.state.data
                    , pin = form.pin.data, email = form.email.data, phoneno = form.phone.data
                    , gstno = form.gstno.data, description = form.description.data, company_id = current_user.activecompany)
        db.session.add(customer)
        db.session.commit()
        flash(f"Customer Created Succefully!","success")
        return redirect(url_for('customers.customerlist'))
    return render_template("customertemplate/addcustomer.html", title="Add Customer", form=form)


@customers.route('/customer/details/<int:customer_id>', methods=['GET','POST'])
@login_required
def showcustomer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.company_id != current_user.activecompany:
        abort(403)
    return render_template('customertemplate/customerdetail.html', title=customer.name, customer = customer)


@customers.route('/customer/<int:customer_id>/deletecustomer', methods=["POST"])
@login_required
def deletecustomer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(customer)
    db.session.commit()
    flash(f"Customer {customer.name} deleted Successfully","success")
    return redirect(url_for('customers.customerlist'))


@customers.route('/customer/details/<int:customer_id>/update', methods=['GET','POST'])
@login_required
def updatecustomer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.company_id != current_user.activecompany:
        abort(403)
    form = CustomerForm()
    form.country.choices+= [(str(country.name), country.name) for country in Countries.query.all()]
    if form.validate_on_submit():
        customer.name = form.name.data
        customer.mailingname = form.mailingname.data
        customer.first = form.first.data
        customer.last = form.last.data
        customer.address = form.address.data
        customer.country = form.country.data
        customer.state = form.state.data
        customer.pin = form.pin.data
        customer.email = form.email.data
        customer.phoneno = form.phone.data 
        customer.gstno = form.gstno.data
        customer.description = form.description.data
        db.session.commit()
        flash(f'Your Customer details has been Updated!', 'success')
        return redirect(url_for('customers.showcustomer', customer_id = customer_id))
    elif request.method == 'GET':
        form.name.data = customer.name 
        form.mailingname.data = customer.mailingname 
        form.first.data = customer.first
        form.last.data = customer.last
        form.address.data = customer.address 
        form.country.data = customer.country 
        form.state.data = customer.state 
        form.pin.data = customer.pin 
        form.email.data = customer.email 
        form.phone.data  = customer.phoneno 
        form.gstno.data = customer.gstno 
        form.description.data = customer.description
    return render_template('customertemplate/updatecustomer.html', title=customer.name, form=form) 
