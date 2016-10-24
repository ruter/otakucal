# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, g
from flask_login import login_user, logout_user, current_user, login_required
from . import app, db, login_manager
from .forms import LoginForm, RegisterForm
from .models import User, Entry, Hobby, HBEntry
from .security import ts

from datetime import datetime, timedelta
import random

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		# Set timezone as UTC+8:00
		g.user.last_login = datetime.utcnow() + timedelta(hours=8)
		db.session.add(g.user)
		db.session.commit()

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	return render_template('500.html'), 500


@app.route('/admin')
@login_required
def admin():
	entries = Entry.query.all().order_by(Entry.id.desc()).paginate(1, 10, False).items
	user_num = User.query.count()
	hobby_num = Hobby.query.count()
	entry_num = Entry.query.count()
	hbentry_num = HBEntry.query.count()
	return render_template('admin.html',
							title='Dashboard',
							user_num=user_num,
							hobby_num=hobby_num,
							entry_num=entry_num,
							hbentry_num=hbentry_num,
							entries=entries)


@app.route('/user')
@login_required
def user():
	pass


@app.route('/hobby')
@login_required
def hobby():
	pass


@app.route('/entry')
@login_required
def entry():
	pass


@app.route('/hbentry')
@login_required
def hbentry():
	pass


@app.route('/edit_entry/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
	pass


@app.route('/del_entry/<int:id>')
@login_required
def del_entry(id):
	pass


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
	user = User.query.filter_by(username=username).first()
	form = RegisterForm()
	if form.validate_on_submit():
		user.email = form.email.data.lower()
		user.password = form.password.data
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('profile', username=g.user.username))
	form.username.data = user.username
	form.email.data = user.email
	return render_template('profile.html',
							title='Profile',
							reg_time=user.reg_time,
							last_login=user.last_login,
							form=form)


@app.route('/register')
def register():
	pass
	

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('admin'))
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data.lower()
		user = User.query.filter_by(email=email).first()
		if user is not None and user.is_correct_password(form.password.data):
			login_user(user, remember=form.remember_me.data)
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('login'))
	return render_template('login.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))