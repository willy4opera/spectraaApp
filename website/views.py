'''
Here We import Flask and other packages
and library needed for our Project
'''
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . models import Services, User
from . import db, createsession_maker
import json
from flask import redirect, url_for


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    services = Services.query.all()
    if services:
        flash('Welcome... Home. ', category='info')
        return render_template(
            "index.html",
            services=services,
            user=current_user)

    else:
        flash('Service Fetch failed', category='error')
        return render_template("index.html", user=current_user)


@views.route('/services', methods=['GET', 'POST'])
def services():
    flash('Location service must be enable', category='info') 

    return render_template("services.html", user=current_user)

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    flash('We are closer to you than you imagine', category='info') 

    return render_template("contact.html", user=current_user)

@views.route('/detail', methods=['GET', 'POST'])
def detail():
    flash('Service Connect Request Successfully Sent!!', category='success') 
    if request.method == 'POST':
        flash('Service Connect Request Successfully Sent!!', category='success') 
        return render_template("detail.html", user=current_user)
    
    return render_template("detail.html", user=current_user)


@views.route('/delete_service', methods=['POST'])
def delete_service():
    # this function expects a JSON from the INDEX.js file
    service = json.loads(request.data)
    serviceId = service['serviceID']
    service = Services.query.get(serviceId)
    if service:
        if service.user_id == current_user.id:
            db.session.delete(service)
            db.session.commit()

    return jsonify({})

@views.route('/connect', methods=['GET', 'POST'])
def connect():
   
    if current_user.is_authenticated:
        flash('Service Connect Request Successfully Sent!!', category='success') 
        return render_template("account.html", user=current_user)
        
    else:
         flash('Kindly Login to request Connect!!', category='error')
         """return redirect(url_for('auth.login'))"""
         return render_template("login2.html", user=current_user)