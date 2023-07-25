from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Category
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # first checking email then password
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            # redirecting user to sign-up page with a flash
            flash('Email does not exist, Want to Sign up?', category='email')
            return redirect(url_for('auth.sign_up'))
    
    return render_template('login.html', user=current_user)

# this route will be only visible when the user logged in
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # redirecting to login page
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists! Try with another Email', category='error')
        elif len(email) < 4:
            flash('Email must be larger than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be larger than 1 character.', category='error')
        elif password1 != password2:
            flash('Password dont match', category='error')
        elif len(password1) < 7:
            flash('Password should consist min 7 characters.', category='error')
        else:
            # hash function to protect passwords
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            # creating default categories when the user sign-up for the first time
            category1 = Category(name='Food', user_id=current_user.id)
            category2 = Category(name='Transportation', user_id=current_user.id)
            category3 = Category(name='Medical', user_id=current_user.id)
            db.session.add(category1)
            db.session.commit()
            db.session.add(category2)
            db.session.commit()
            db.session.add(category3)
            db.session.commit()
            flash('Successfully Account created!!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template('sign_up.html', user=current_user)