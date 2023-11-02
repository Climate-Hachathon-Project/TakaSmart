from flask import render_template, url_for, flash, redirect, request, jsonify
from ..models import User, WastePost, RecyclerView
from ..forms import RegistrationForm, LoginForm, WastePostForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from . import views
from .. import db

@views.route('/')
@views.route('/home')
def home():
    # Display the home page with some information
    return render_template('index.html')


@views.route('/post_waste', methods=['GET', 'POST'])
@login_required
def post_waste():
    # Allow users to post waste details
    form = WastePostForm()
    if form.validate_on_submit():
        # Create a new WastePost instance and add to the database
        waste_post = WastePost(title=form.title.data, description=form.description.data, 
                               quantity=form.quantity.data, author=current_user)
        db.session.add(waste_post)
        db.session.commit()
        flash('Your waste has been posted!')
        return redirect(url_for('home'))
    return render_template('post_waste.html', title='Post Waste', form=form)

@views.route('/waste/<int:waste_post_id>')
def waste_details(waste_post_id):
    # Show details of a particular waste post
    waste_post = WastePost.query.get_or_404(waste_post_id)
    return render_template('waste_details.html', title=waste_post.title, post=waste_post)

@views.route('/dashboard')
@login_required
def dashboard():
    # Dashboard view for users to manage their posts and interactions
    if current_user.is_recycler:
        # Show a different dashboard for recyclers
        return render_template('recycler_dashboard.html', title='Recycler Dashboard')
    else:
        return render_template('user_dashboard.html', title='Dashboard')

# ... More routes as needed for your application

# Remember to initialize your db and login manager in your main application file
