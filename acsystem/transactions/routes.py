from flask import Blueprint, flash, redirect, url_for, render_template, request, jsonify
from datetime import datetime
from acsystem.models import Sales, SalesItem, Customer, Product
from acsystem.transactions.forms import SalesForm, SalesItemForm
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
    form2 = SalesItemForm()
    form1.customer.choices+= [(str(customer.id), customer.name) for customer in Customer.query.filter_by(company_id = current_user.activecompany).all()]
    form2.product.choices+= [(str(product.id), product.name) for product in Product.query.filter_by(company_id = current_user.activecompany).all()]
    if form1.validate_on_submit():
        pass
    elif request.method == 'GET':
        dt = datetime.utcnow()
        form1.date.data = datetime(dt.year, dt.month, dt.day)
    return render_template('transactiontemplate/addinvoice.html', title='Create Invoice', form1=form1, form2= form2)

@transactions.route('/invoice/loadinvoicedetails/<product_id>')
@login_required
def loaddetails(product_id):
    product = Product.query.get_or_404(product_id)
    productobj = {
        "quantity":product.quantity,
        "rate" : product.rate
    }
    return jsonify({'product':productobj})
    