from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import uuid as uuid
from werkzeug.utils import secure_filename
from . import save_profile





ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodby! See you soon', category='info')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('FName')
        last_name = request.form.get('LName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone_num = request.form.get('Phone_Number')
        address = request.form.get('address')
        dateofbirth = request.form.get('DOD')


        if 'profile_pic' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        profile_pic = request.files['profile_pic']
        # if user does not select file, browser also
        # submit an empty part without filename
        if profile_pic.filename == '':
            flash('No selected file', category='error') 
            return redirect(request.url)
        
        pic_name = save_profile(profile_pic)



        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')

        
        elif request.files['profile_pic'].filename == '':
            flash('Please upload profile Picture', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, dateofbirth=dateofbirth, address=address, phone_num=phone_num,
                            last_name=last_name, profile_pic=pic_name, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha1', salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))
    
    

       

    return render_template("register.html", user=current_user)

@auth.route('/account', methods=['GET', 'POST'] )
@login_required
def user_account():
    id = current_user.id

    return render_template('account.html', user=current_user)

