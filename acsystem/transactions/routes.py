from flask import Blueprint, flash, redirect, url_for, render_template, request, jsonify, abort
from datetime import datetime
from acsystem.models import Sales, SalesItem, Customer, Product, Company
from acsystem.transactions.forms import SalesForm
from flask_login import login_required, current_user

transactions = Blueprint('transactions',__name__)

@transactions.route('/invoice')
@login_required
def invoice():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    sales = Sales.query.filter_by(company_id = current_user.activecompany).all()
    return render_template('transactiontemplate/invoice.html', title='Invoice', sales = sales)

@transactions.route('/invoice/createinvoice', methods=['GET','POST'])
@login_required
def createinvoice():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))

    form1 = SalesForm()
    for item in form1.items:
        item.product.choices += [(str(prod.id),prod.name) for prod in Product.query.filter_by(company_id = current_user.activecompany).all()]
    if form1.validate_on_submit():
        print("First Form Validated")
        for entry in form1.items.entries:
            print(entry.product.data)
            print(entry.quantity.data)
            print(entry.rate.data)
        flash(f"Invoice Generated","success")
        return redirect(url_for('transactions.invoice'))
    print(form1.errors)
    if request.method == 'GET':
        dt = datetime.utcnow()
        form1.date.data = datetime(dt.year, dt.month, dt.day)
        lastentry = Company.query.get_or_404(current_user.activecompany)
        form1.invoiceno.data = lastentry.invoiceno+1
    return render_template('transactiontemplate/addinvoice.html', title='Create Invoice', form1=form1)

@transactions.route('/invoice/loadcustomer')
@login_required
def loadcustomer():
    custarr = []
    for c in Customer.query.filter_by(company_id = current_user.activecompany).all():
        cust = {}
        cust["id"] = c.id
        cust["name"] = c.name
        custarr.append(cust)
    return jsonify({'customer': custarr})

@transactions.route('/invoice/loadproductdetail/<product_id>')
@login_required
def loadproductdetail(product_id):
    product = Product.query.get_or_404(product_id)
    if(product.company_id != current_user.activecompany):
        abort(403);
    productobj = {
        "quantity":product.quantity,
        "rate" : product.rate,
        "unit": product.unitname
    }
    return jsonify({'product':productobj})

@transactions.route('/invoice/loadcustomerdetail/<customer_id>')
@login_required
def loadcustomerdetail(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if(customer.company_id != current_user.activecompany):
        abort(403);
    customerobj = {
        "name":customer.name,
        "mailingname" : customer.mailingname,
        "address": customer.address,
        "country": customer.country,
        "state": customer.state,
        "pin": customer.pin,
        "email": customer.email,
        "phone": customer.phoneno,
        "gstno": customer.gstno,
        "currentbalance": customer.currentbalance
    }
    return jsonify({'customer':customerobj})
    