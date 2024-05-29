'''
Here, we import the require packages and library for
Our auth module.
'''
from flask import Blueprint, render_template, request, flash
from flask import redirect, url_for, jsonify
from .models import User, Services
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import uuid as uuid
from werkzeug.utils import secure_filename
from . import save_profile
from . import geocode_location


'''
Here, we defined the set of allowed file extention
for uploading to the server.
'''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    flash('Location service must be enable', category='info')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        # Simple validation
        if latitude is None or longitude is None:
            return jsonify(
                {'success': False, 'message': 'Missing information'}), 400
        api_key = '250b35f249134d77af0b6a9348598154'
        location = geocode_location(latitude, longitude, api_key)

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                user.location = location
                db.session.commit()
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

# The sign up route.


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    flash('Location service must be enable', category='info') 
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('FName')
        last_name = request.form.get('LName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone_num = request.form.get('Phone_Number')
        address = request.form.get('address')
        dateofbirth = request.form.get('DOD')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        # Simple validation
        if latitude is None or longitude is None:
            return jsonify(
                {'success': False, 'message': 'Missing information'}), 400
        api_key = '250b35f249134d77af0b6a9348598154'
        location = geocode_location(latitude, longitude, api_key)

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
        user_mobile = User.query.filter_by(phone_num=phone_num).first()
        if user:
            flash('Email already exists.', category='error')

        elif request.files['profile_pic'].filename == '':
            flash('Please upload profile Picture', category='error')

        elif user_mobile:
            flash('Phone Number Already Exist', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash(
                'First name must be greater than 1 character.',
                category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email,
                dateofbirth=dateofbirth,
                address=address,
                phone_num=phone_num,
                last_name=last_name,
                profile_pic=pic_name,
                first_name=first_name,
                location=location,
                password=generate_password_hash(
                    password1,
                    method='pbkdf2:sha1',
                    salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("register.html", user=current_user)


@auth.route('/account', methods=['GET', 'POST'])
@login_required
def user_account():

    id = current_user.id

    return render_template('account.html', user=current_user)


@auth.route('/add-service', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        id = current_user.id
        title = request.form.get('title')
        description = request.form.get('description')
        cost = request.form.get('cost')

        if 'service_banner' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        service_banner = request.files['service_banner']
        # if user does not select file, browser also
        # submit an empty part without filename
        if service_banner.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)

        service_banner = save_profile(service_banner)
        new_service = Services(
            service_title=title,
            description=description,
            cost=cost,
            service_banner=service_banner)
        db.session.add(new_service)
        db.session.commit()
        flash('Service Added successfully!', category='success')
        return redirect(url_for('auth.add_service'))
    return render_template('addservices.html', user=current_user)


