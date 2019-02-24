from flask import Blueprint, render_template, url_for, flash, redirect, abort, request
from acsystem import bcrypt, db
from acsystem.company.forms import CompanyForm, UpdateCompanyForm
from acsystem.models import Company, Countries
from flask_login import current_user, login_required
from datetime import datetime

company = Blueprint('company', __name__)

@company.route("/company")
@login_required
def companies():
    companies = Company.query.filter_by(owner = current_user).order_by(Company.datecreated.desc())
    activecomp = Company.query.get(current_user.activecompany)
    return render_template("companytemplate/companies.html", title="Company", companies = companies, activecomp = activecomp)


@company.route('/activate/<int:compid>')
def activatecompany(compid):
    comp = Company.query.get_or_404(compid)
    if comp.owner != current_user:
        abort(403)
    current_user.activecompany = compid
    db.session.commit()
    return redirect(url_for('users.dashboard'))


@company.route('/company/<int:compid>/deletecompany', methods=["POST"])
@login_required
def deletecompany(compid):
    company = Company.query.get_or_404(compid)
    if company.owner != current_user:
        abort(403)
    db.session.delete(company)
    current_user.activecompany = 0
    db.session.commit()
    flash(f"Company {company.companyname} deleted Successfully","success")
    return redirect(url_for('users.dashboard'))


@company.route('/company/details/<int:compid>', methods=['GET','POST'])
@login_required
def showcompany(compid):
    company = Company.query.get_or_404(compid)
    if company.owner != current_user:
        abort(403)
    return render_template('companytemplate/companydetail.html', title=company.companyname, company = company)


@company.route("/company/addcompany", methods=['GET','POST'])
@login_required
def addcompany():
    companies = Company.query.filter_by(owner = current_user).all()
    if len(companies)>=5:
        flash(f"You have reached the maximum limit for creating companies Under this account!","info")
        return redirect(url_for('company.companies'))
    if len(companies)>=4:
        flash(f"You can only create 5 companies Under this account!","warning")
    form = CompanyForm()
    form.country.choices+= [(str(country.name), country.name) for country in Countries.query.all()]
    if form.validate_on_submit():
        company = Company(companyname = form.name.data, mailingname = form.mailingname.data
                    , address = form.address.data, country = form.country.data, state = form.state.data, booksbegin = form.booksbegin.data
                    , pin = form.pin.data, email = form.email.data, phoneno = form.phone.data, financialyear = form.financialyear.data
                    , website = form.website.data, gstno = form.gstno.data, description = form.description.data, owner = current_user)
        db.session.add(company)
        db.session.commit()
        flash(f"Company Created Succefully!","success")
        return redirect(url_for('company.companies'))
    elif request.method == 'GET':
        dt = datetime.utcnow()
        form.financialyear.data = datetime(dt.year, 4,1)
        form.booksbegin.data = dt
    return render_template("companytemplate/addcompany.html", title="Add Company", form=form)


@company.route('/company/details/<int:compid>/update', methods=['GET','POST'])
@login_required
def updatecompany(compid):
    company = Company.query.get_or_404(compid)
    if company.owner != current_user:
        abort(403)
    form = UpdateCompanyForm()
    form.country.choices+= [(str(country.name), country.name) for country in Countries.query.all()]
    if form.validate_on_submit():
        company.companyname = form.name.data
        company.mailingname = form.mailingname.data
        company.address = form.address.data
        company.country = form.country.data
        company.state = form.state.data
        company.pin = form.pin.data
        company.email = form.email.data
        company.phoneno = form.phone.data 
        company.website = form.website.data
        company.financialyear = form.financialyear.data
        company.booksbegin = form.booksbegin.data
        company.gstno = form.gstno.data
        company.description = form.description.data
        db.session.commit()
        flash(f'Your Company details has been Updated!', 'success')
        return redirect(url_for('company.showcompany', compid = compid))
    elif request.method == 'GET':
        form.name.data = company.companyname 
        form.mailingname.data = company.mailingname 
        form.address.data = company.address 
        form.country.data = company.country 
        form.state.data = company.state 
        form.pin.data = company.pin 
        form.email.data = company.email 
        form.phone.data  = company.phoneno 
        form.website.data = company.website 
        form.financialyear.data = company.financialyear
        form.booksbegin.data = company.booksbegin
        form.gstno.data = company.gstno 
        form.description.data = company.description
    return render_template('companytemplate/updatecompany.html', title=company.companyname, form=form) 


