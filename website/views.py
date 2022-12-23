from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Messages, User
from datetime import datetime
from operator import attrgetter
from . import db
import os

views = Blueprint('views', __name__)

PHOTO_FOLDER = 'website/static/photos/'
UPLOAD_FOLDER = 'website/static/profile/'
ALLOWED_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    data = User.query.all()
    return render_template('dashboard.html', users=data, user=current_user)

@views.route('/message/<username>/', methods=['GET'])
@login_required
def message(username):
    data = User.query.filter_by(username=username).first()
    from_msg = Messages.query.filter(Messages.from_user==current_user.username, Messages.to_user==data.username).all()
    to_msg = Messages.query.filter(Messages.from_user==data.username, Messages.to_user==current_user.username).all()
    for i in to_msg:
        i.seen = True
    db.session.commit()
    msg = from_msg + to_msg
    msg.sort(key=attrgetter('id'))
    return render_template('message.html', to_user=data, messages=msg, user=current_user)

@views.route('/send', methods=['POST'])
@login_required
def send():
    if request.method == 'POST':
        from_user = request.form.get('from_user')
        to_user = request.form.get('to_user')
        message = request.form.get('message')
        photo = request.files.get('photo')
        if photo.filename:
            _ , b = os.path.splitext(secure_filename(photo.filename))
            if b.lower() in ALLOWED_FORMATS:
                filename = os.path.join(PHOTO_FOLDER, secure_filename(photo.filename))
                photo.save(filename)
                db.session.add(Messages(from_user=from_user, to_user=to_user, message=message, photo=filename[7:]))
                db.session.commit()
            else:
                flash("Invalid File format :) only images are allowed", category='error')
        else:
            db.session.add(Messages(from_user=from_user, to_user=to_user, message=message))
            db.session.commit()
    return redirect(url_for("views.message", username=to_user))


@views.route('/friends', methods=['GET', 'POST'])
def friends():
    msg = Messages.query.filter(Messages.from_user==current_user.username).all()

    return render_template('messages.html', messages=msg, user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        user = current_user
        user.name = request.form.get('name')
        user.bio = request.form.get('bio')
        user.gender = request.form.get('gender')
        dob = request.form.get('dob').split('-')
        user.dob = datetime(int(dob[0]), int(dob[1]), int(dob[2]))
        user.country = request.form.get('country')
        user.state = request.form.get('state')
        if 'profile' in request.files:
            profile = request.files['profile']
            filename = os.path.join(UPLOAD_FOLDER, secure_filename(profile.filename))
            _ , b = os.path.splitext(filename)
            if b.lower() in ALLOWED_FORMATS:
                if os.path.exists('website' + user.profile):
                    db.session.commit()
                else:
                    profile.save(filename)
                    user.profile = filename[7:]
                    db.session.commit()
                flash(f"{user.name}'s Details Updated Successfully", category='success')
        else:
            db.session.commit()
            flash(f"{user.name}'s Details Updated Successfully", category='success')

    return render_template('profile.html', user=current_user)


# @views.route('/msgview', methods=['GET', 'POST'])
# def msgview():
#     # data = Contact.query.all()
#     return render_template('contact.html', msgdata=data, user=current_user)

# @views.route('/delmsg/<id>/', methods=['GET', 'POST'])
# @login_required
# def delmsg(id):
#     # data = Contact.query.get(id)
#     # db.session.delete(data)
#     # db.session.commit()
#     flash("Message Deleted Successfully", category='success')
#     return redirect(url_for('views.msgview'))


# @views.route('/chair')
# def chair():
#     data = Chairs.query.all()
#     return render_template('chair.html', chairs=data)

# @views.route('/admin', methods=['GET', 'POST'])
# @login_required
# def admin():
#     data = Chairs.query.all()
#     return render_template('admin.html', chairs=data, user=current_user)

@views.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    if request.method == 'POST':
        title = request.form.get('title')

        if 'cover' not in request.files:
            flash("No file in form", category='error')
            return redirect(request.url)

        file = request.files['cover']
        desc = request.form.get('description')
        
        if file.filename == '':
            flash("No file selected", category='error')
            return redirect(request.url)
        else:
            _ , b = os.path.splitext(secure_filename(file.filename))
            if b.lower() in ALLOWED_FORMATS:
                filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
                file.save(filename)
                # db.session.add(Chairs(title=title, cover=filename[8:], description=desc))
                # db.session.commit()
                flash("Chair Added Successfully", category='success')
            else:
                flash("Invalid File format :) only images are allowed", category='error')
        
    return redirect(url_for('views.admin'))

@views.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        # data = Chairs.query.get(request.form.get('sno'))
        # data.title = request.form.get('title')
        # data.description = request.form.get('description')
        file = request.files['cover']

        if file.filename == '':
            db.session.commit()
            flash("Chair Updated Successfully", category='success')
            return redirect(url_for('views.admin'))
        else:
            filename = os.path.join(PHOTO_FOLDER, secure_filename(file.filename))
            _ , b = os.path.splitext(filename)
            if b.lower() in ALLOWED_FORMATS:
                # if os.path.exists('website/' + data.cover):
                #     os.remove('website/' + data.cover)
                # file.save(filename)
                # flash("Image Updated Successfully", category='success')
                # data.cover = filename[8:]
                # db.session.commit()
                flash("Chair Updated Successfully", category='success')

            else:
                flash("Invalid File format only images are allowed", category='error')

    return redirect(url_for('views.admin'))


@views.route('/delete/<sno>/', methods=['GET', 'POST'])
@login_required
def delete(sno):
    # data = Chairs.query.get(sno)
    # if os.path.exists('website/' + data.cover):
    #     os.remove('website/' + data.cover)
    # db.session.delete(data)
    db.session.commit()
    flash("Chair Deleted Successfully", category='success')
    return redirect(url_for('views.admin'))




@views.route('/pdfreader', methods=['GET'])
def pdfreader():
    data = Messages.query.all()
    return render_template('reader.html', data=data)