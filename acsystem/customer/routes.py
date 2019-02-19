from flask import Blueprint, render_template, url_for, current_app, flash, redirect, abort
from flask_login import login_required, current_user
from acsystem import db
from acsystem.models import Customer, Countries, Company
from acsystem.customer.forms import CustomerForm

customers = Blueprint('customers', __name__)

@customers.route('/customer')
@login_required
def customerlist():
    customers = Customer.query.filter_by(company_id = current_user.activecompany).all()
    return render_template('customertemplate/customerlist.html', title='Customers', customers=customers)


@customers.route("/addcustomer", methods=['GET','POST'])
@login_required
def addcustomer():
    form = CustomerForm()
    form.country.choices+= [(str(country.name), country.name) for country in Countries.query.all()]
    if form.validate_on_submit():
        customer = Customer(name = form.name.data, first= form.first.data, last = form.last.data
                    , mailingname = form.mailingname.data
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
