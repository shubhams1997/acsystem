from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from acsystem import db
from acsystem.models import Productcategory, Unit
from acsystem.product.forms import ProductCategoryForm, UnitForm

products = Blueprint("products",__name__)

@products.route("/product")
@login_required
def product():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    return render_template('producttemplate/products.html', title="Products");


@products.route("/category_unit", methods=['GET','POST'])
@login_required
def categoryunit():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    form = ProductCategoryForm()
    form2 = UnitForm()
    if form2.validate_on_submit():
        unit = Unit(symbol = form2.symbol.data, name = form2.name.data, company_id = current_user.activecompany)
        db.session.add(unit)
        db.session.commit()
        flash(f"Unit Added Successfully!","success")
        return redirect(url_for("products.categoryunit"))

    if form.validate_on_submit():
        category = Productcategory(name = form.name.data, company_id = current_user.activecompany)
        db.session.add(category)
        db.session.commit()
        flash(f"Product Category {form.name.data} Added Successfully!","success")
        return redirect(url_for('products.categoryunit'))
    pcs = Productcategory.query.filter_by(company_id = current_user.activecompany).all()

    units = Unit.query.filter_by(company_id = current_user.activecompany).all()
    return render_template('producttemplate/categoryunit.html', title="Product Categories and Units", form=form, form2=form2, pcs=pcs, units=units)


@products.route("/category_unit/delete/category/<int:pc_id>", methods=['POST'])
@login_required
def deleteproductcategory(pc_id):
    pc = Productcategory.query.get_or_404(pc_id);
    if pc.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(pc)
    db.session.commit()
    flash(f"{pc.name} Deleted Successfully.","success")
    return redirect(url_for('products.categoryunit'))


@products.route("/category_unit/delete/unit/<int:unit_id>", methods=['POST'])
@login_required
def deleteunit(unit_id):
    unit = Unit.query.get_or_404(unit_id);
    if unit.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(unit)
    db.session.commit()
    flash(f"Unit {unit.symbol} Deleted Successfully.","success")
    return redirect(url_for('products.categoryunit'))
