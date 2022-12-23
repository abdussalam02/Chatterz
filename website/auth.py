from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from .models import User
from . import db
import os

auth = Blueprint('auth', __name__)

UPLOAD_FOLDER = 'website/static/profile/'
ALLOWED_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']

@auth.route('register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print(password)

        if 'profile' not in request.files:
            flash("No Profile Added", category='error')
            return redirect(request.url)
        
        profile = request.files['profile']
        
        if profile.filename == '':
            flash("No Profile Picture selected", category='error')
            return redirect(request.url)

        if len(name) < 3:
            flash("Name should be greater than 3 characters", category='error')
        elif User.query.get(username):
            flash("Username already taken please try with another one", category='error')
        elif len(email) < 6:
            flash("Email should be greater than 6 character including @gmail.com", category='error')
        elif len(phone) < 8:
            flash("Phone should be greater than 8 Number", category='error')
        elif len(password) < 8:
            flash("Password should be greater than 8 character", category='error')
        elif password != password2:
            flash("Password and Confirm Password doesn't match", category='error')
        else:
            _ , b = os.path.splitext(secure_filename(profile.filename))
            if b.lower() in ALLOWED_FORMATS:
                filename = os.path.join(UPLOAD_FOLDER, secure_filename(profile.filename))
                profile.save(filename)
                user = User(profile=filename[7:], username=username, name=name, email=email, phone=phone, password=generate_password_hash(password, method='sha256'))
                db.session.add(user)
                db.session.commit()
                flash("Account created successfully, you can Login :)", category='success')
            else:
                flash("Invalid File format :) only images are allowed", category='error')
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if len(password) < 8:
            flash("Enter the correct password", category='error')
        if user:
            if check_password_hash(user.password, password):
                if user.is_admin:
                    user.logged = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=True)
                    flash(f"You are successfully logged in {user.name}", category='success')
                    return redirect(url_for('views.dashboard'))
                else:
                    user.logged = True
                    # db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=True)
                    flash(f"You are successfully logged in {user.name}", category='success')
                    return redirect(url_for('views.dashboard'))
            else:
                flash(f"Wrong password {user.name}, Try again!", category='error')
        else:
            flash("You do not have an account please create one", category='error')
            return redirect(url_for('auth.register'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    user = current_user
    user.logged = False
    db.session.commit()
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for('auth.login'))