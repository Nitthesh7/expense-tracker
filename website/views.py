from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .models import Entry, Category
from . import db
import json

# every route here requires user login, it will automatically redirect to login page if not logged in
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    # expense table can be seen (#TODO: add filters like year-wise, category-wise and any other)
    return render_template('home.html', user=current_user)

@views.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        date = request.form.get('date')
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description')

        # only description is optional
        if amount == '':
            flash('Amount cannot be none.', category='error')
        elif category == '':
            flash('Category cannot be none.', category='error')
        elif date == '':
            flash('Date cannot be none.', category='error')
        else:
            # changing the format of data per database requirement
            date_format = "%Y-%m-%d"
            new_entry = Entry(amount=float(amount), category=category, description=description, 
                                user_id=current_user.id, date=datetime.strptime(date, date_format))
            db.session.add(new_entry)
            db.session.commit()
            flash('Entry added!!', category='success')
    return render_template('add.html', user=current_user)

# deleting entries using entry id
@views.route('/delete-entry/<int:id>')
@login_required
def delete_entry(id):
    entry = Entry.query.get_or_404(int(id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted!!", "success")
    return redirect(url_for("views.home"))       

# customize page to add/ delete categories if required
# TODO: add more customization like maybe change email/ password?
@views.route('/customize', methods=['GET', 'POST'])
@login_required
def customize():
    if request.method == 'POST':
        category = request.form.get('category')

        if category == '':
            flash('Category should consist atleast more than one character.', category='error')
        else:
            new_category = Category(name=category, user_id=current_user.id)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added!!', category='success')
    return render_template('customize.html', user=current_user)

# similar to entry deleting but for categories in customize page
@views.route('/delete-category/<int:id>')
@login_required
def delete_category(id):
    category = Category.query.get_or_404(int(id))
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted!!", "success")
    return redirect(url_for("views.customize"))   

# TODO: report/ plots with different filters
@views.route('/summary')
@login_required
def summary():
    return render_template('summary.html', user=current_user)