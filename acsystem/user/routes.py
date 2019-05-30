from flask import Blueprint, render_template, url_for, flash, redirect, request, session, jsonify
from acsystem import bcrypt, db
from acsystem.user.forms import LoginForm, RegisterForm, UpdateUserForm
from acsystem.models import User, Company
from flask_login import login_user, current_user, login_required, logout_user

users = Blueprint('users',__name__)


@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You loged in Successfully!","success")
            return redirect(url_for('users.dashboard'))
        else:
            flash("Login Unsuccessful!", "warning")
    return render_template("usertemplate/login.html", title = "login", form=form)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(form.firstname.data, form.lastname.data, form.email.data, 0, hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your Account for {form.firstname.data} has Been Created Successfully!","success")
        login_user(user)
        return redirect(url_for('company.companies'))
    return render_template('usertemplate/register.html', title = "register", form=form)


@users.route("/dashboard")
@login_required
def dashboard():
    activecomp = Company.query.get(current_user.activecompany)
    return render_template("usertemplate/dashboard.html", title="Dashboard", activecomp=activecomp)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/user/accountinfo')
@login_required
def account():
    return render_template('usertemplate/accountinfo.html', title="Account")


@users.route('/user/accountinfo/update', methods=['GET','POST'])
@login_required
def updateuser():
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.first = form.firstname.data 
        current_user.last = form.lastname.data
        current_user.email = form.email.data
        current_user.phone = form.phoneno.data
        db.session.commit()
        flash(f'Your details has been Updated!', 'success')
        return redirect(url_for('users.account'))

    if request.method == "GET":
        form.firstname.data = current_user.first
        form.lastname.data = current_user.last
        form.email.data = current_user.email
        form.phoneno.data = current_user.phone
    return render_template('usertemplate/update.html', title='Update', form=form)


@users.route('/user/deleteuser', methods=['GET','POST'])
@login_required
def deleteuser():
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('users.register'))
    
