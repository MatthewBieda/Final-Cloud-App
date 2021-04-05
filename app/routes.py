from re import error
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime
import requests
import json

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        year = request.form.get('year')
        if year > '2005':
            return redirect(f'/{year}')
        else:
            return "Please enter a year between 2006 and 2019"

    if request.method == 'GET':
        return render_template('index.html', title='Home')

@app.route('/<year>', methods=['GET'])
def get_year(year):
    if current_user.is_authenticated:
        data = requests.get(f"https://api.tfl.gov.uk/AccidentStats/{year}")
        jsondata = data.json()
        listed = []

        for line in jsondata:
            listed.append([line['date'], line['severity'], line['borough'], [x['type'] for x in line['vehicles']], len(line['casualties'])])
        listed = listed[:50]
        return render_template('accident_data.html', listed=listed, year=year)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/index/user/<username>/delete', methods=['GET','POST', 'DELETE'])
@login_required
def delete(username):
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
            return redirect('/index')
        return redirect('/404')
 
    return render_template('delete.html', user=user)

@app.route('/update_profile', methods=['GET', 'POST', 'PUT'])
@login_required
def update_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('update_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('update_profile.html', title='Update Profile', form=form)




