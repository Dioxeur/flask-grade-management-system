from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from website.models import User
from website.forms import LoginForm, SignUpForm
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            session.permanent = True
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password.', category='error')
    
    return render_template("login.html", user=current_user, form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        first_name = form.first_name.data.strip()
        password = form.password.data
        role = form.role.data

        new_user = User(
            email=email,
            first_name=first_name,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created successfully!', category='success')
        return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user, form=form)




