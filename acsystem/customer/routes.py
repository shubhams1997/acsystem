from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
from acsystem.models import Customer, Countries
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
    # if form.validate_on_submit():
    #     company = Company(companyname = form.name.data, mailingname = form.mailingname.data
    #                 , address = form.address.data, country = form.country.data, state = form.state.data
    #                 , pin = form.pin.data, email = form.email.data, phoneno = form.phone.data
    #                 , website = form.website.data, gstno = form.gstno.data, description = form.description.data, owner = current_user)
    #     db.session.add(company)
    #     db.session.commit()
    #     flash(f"Company Created Succefully!","success")
    #     return redirect(url_for('company.companies'))
    return render_template("customertemplate/addcustomer.html", title="Add Customer", form=form)
