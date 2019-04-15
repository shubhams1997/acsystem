from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from acsystem import db
from acsystem.models import Productcategory, Unit, Product
from acsystem.product.forms import ProductCategoryForm, UnitForm, ProductForm, ProductUpdateForm

products = Blueprint("products",__name__)

@products.route("/product")
@login_required
def product():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    productlist = Product.query.filter_by(company_id = current_user.activecompany).all()
    return render_template('producttemplate/products.html', title="Products", productlist = productlist);

@products.route("/product/addproduct", methods=['GET','POST'])
@login_required
def addproduct():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    form = ProductForm()
    form.category.choices += [(str(category.id), category.name) for category in Productcategory.query.filter_by(company_id = current_user.activecompany).all()]
    form.unit.choices += [(str(unit.id), unit.symbol) for unit in Unit.query.filter_by(company_id = current_user.activecompany).all()]
    if form.validate_on_submit():
        unit = Unit.query.get(int(form.unit.data))
        category = Productcategory.query.get(form.category.data)
        newproduct = Product(name = form.name.data, category = category.id
                , unit = unit.id , quantity = form.quantity.data, rate = form.rate.data
                , salesprice = form.salesprice.data, company_id = current_user.activecompany)
        db.session.add(newproduct)
        db.session.commit()
        flash(f"Product {form.name.data} is Added Successfully!",'success')
        return redirect(url_for('products.product'))
    return render_template('producttemplate/addproduct.html', title = "Add Product", form=form)


@products.route('/product/<int:product_id>/detail')
@login_required
def productdetail(product_id):
    prod = Product.query.get_or_404(product_id)
    if prod.company_id != current_user.activecompany:
        abort(403)
    return render_template('producttemplate/productdetail.html', title=prod.name, prod=prod)


@products.route('/product/<int:product_id>/deleteproduct', methods=["POST"])
@login_required
def deleteproduct(product_id):
    prod = Product.query.get_or_404(product_id)
    if prod.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(prod)
    db.session.commit()
    flash(f"Product {prod.name} deleted Successfully","success")
    return redirect(url_for('products.product'))


@products.route('/product/<int:product_id>/updateproduct', methods=['GET','POST'])
@login_required
def updateproduct(product_id):
    prod = Product.query.get_or_404(product_id)
    if prod.company_id != current_user.activecompany:
        abort(403)
    form = ProductUpdateForm()
    form.category.choices += [(str(category.id), category.name) for category in Productcategory.query.filter_by(company_id = current_user.activecompany).all()]
    form.unit.choices += [(str(unit.id), unit.symbol) for unit in Unit.query.filter_by(company_id = current_user.activecompany).all()]
    if form.validate_on_submit():
        unit = Unit.query.get(int(form.unit.data))
        category = Productcategory.query.get(form.category.data)
        prod.name = form.name.data
        prod.category = category.id
        prod.quantity = form.quantity.data
        prod.unit = unit.id
        prod.rate = form.rate.data
        prod.salesprice = form.salesprice.data
        db.session.commit()
        flash(f"Product details updated.","success")
        return redirect(url_for('products.productdetail', product_id = prod.id))
    elif request.method == "GET":
        form.vdname.data = prod.name
        form.name.data = prod.name
        form.category.data = str(prod.category)
        form.quantity.data = prod.quantity
        form.unit.data = str(prod.unit)
        form.rate.data = prod.rate
        form.salesprice.data = prod.salesprice
    return render_template('producttemplate/updateproduct.html', title=prod.name, form=form)



@products.route("/category_unit", methods=['GET','POST'])
@login_required
def categoryunit():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    form = ProductCategoryForm()
    form2 = UnitForm()
    if form2.validate_on_submit() and form2.submit.data:
        unit = Unit(symbol = form2.symbol.data, name = form2.name.data, company_id = current_user.activecompany)
        db.session.add(unit)
        db.session.commit()
        flash(f"Unit Added Successfully!","success")
        return redirect(url_for("products.categoryunit"))

    if form.validate_on_submit() and form.submit.data:
        category = Productcategory(name = form.category_name.data, company_id = current_user.activecompany)
        db.session.add(category)
        db.session.commit()
        flash(f"Product Category {form.category_name.data} Added Successfully!","success")
        return redirect(url_for('products.categoryunit'))
    pcs = Productcategory.query.filter_by(company_id = current_user.activecompany).all()

    units = Unit.query.filter_by(company_id = current_user.activecompany).all()
    return render_template('producttemplate/categoryunit.html', title="Product Categories and Units", form=form, form2=form2, pcs=pcs, units=units)


@products.route("/category_unit/delete/category/<int:pc_id>", methods=['POST'])
@login_required
def deleteproductcategory(pc_id):
    pc = Productcategory.query.get_or_404(pc_id)
    if pc.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(pc)
    db.session.commit()
    flash(f"{pc.name} Deleted Successfully.","success")
    return redirect(url_for('products.categoryunit'))


@products.route("/category_unit/delete/unit/<int:unit_id>", methods=['POST'])
@login_required
def deleteunit(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    if unit.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(unit)
    db.session.commit()
    flash(f"Unit {unit.symbol} Deleted Successfully.","success")
    return redirect(url_for('products.categoryunit'))
