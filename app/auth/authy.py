# Inside app/auth/auth.py

from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from . import  auth
from .. import db


@auth.route('/signup', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    form = RegistrationForm()  # Assuming you have a WTForms form that handles registration
    if form.validate_on_submit():  # Check if the form submission is valid
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create a new user
            new_user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully', 'success')
            return redirect(url_for('auth.login'))  # Make sure this endpoint is correct
        else:
            flash('Username already exists', 'error')

    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Instantiate your form
    if form.validate_on_submit():
        user 
        login_user()
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/logout')
def logout():
    # Log out the current user
    logout_user()
    return redirect(url_for('home'))

# Add more auth related routes if needed
