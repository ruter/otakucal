# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, g
from flask_login import login_user, logout_user, current_user, login_required
from . import app, db, login_manager
from .forms import LoginForm, RegisterForm, HobbyForm, EntryForm, HBEntryForm
from .models import User, Entry, Hobby, HBEntry
from .security import ts
from app import apis

from datetime import datetime, timedelta


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

@app.route('/')
@app.route('/admin')
@login_required
def admin():
	try:
		entries = Entry.query.order_by(Entry.id.desc()).paginate(1, 10, False).items
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
	except:
		return render_template('admin.html')


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
	form = RegisterForm()
	if form.validate_on_submit():
		email = form.email.data.lower()
		u = User(
			username=form.username.data, 
			email=email, 
			password=form.password.data)
		db.session.add(u)
		db.session.commit()
		return redirect(url_for('user'))
	users = User.query.all()
	return render_template('user.html', title='Users', form=form, users=users)


@app.route('/hobby', methods=['GET', 'POST'])
@login_required
def hobby():
	form = HobbyForm()
	if form.validate_on_submit():
		hobby = Hobby(hobby=form.hobby.data)
		db.session.add(hobby)
		db.session.commit()
		return redirect(url_for('hobby'))
	hobbies = Hobby.query.order_by(Hobby.id.desc())
	return render_template('hobby.html', title='Hobbies', form=form, hobbies=hobbies)

@app.route('/edit_hobby/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_hobby(id):
	form = HobbyForm()
	hobby = Hobby.query.filter_by(id=id).first()
	if form.validate_on_submit():
		hobby.hobby = form.hobby.data
		db.session.add(hobby)
		db.session.commit()
		return redirect(url_for('hobby'))
	form.hobby.data = hobby.hobby
	return render_template('edit_hobby.html', title='Edit Hobby', form=form)

@app.route('/del_hobby/<int:id>')
@login_required
def del_hobby(id):
	try:
		hobby = Hobby.query.filter_by(id=id).first()
		db.session.delete(hobby)
		db.session.commit()
		return redirect(url_for('hobby'))
	except:
		return redirect(url_for('hobby'))


@app.route('/entry', methods=['GET', 'POST'])
@login_required
def entry():
	form = EntryForm()
	if form.validate_on_submit():
		entry = Entry(good=form.good.data, bad=form.bad.data)
		db.session.add(entry)
		db.session.commit()
		return redirect(url_for('entry'))
	entries = Entry.query.order_by(Entry.id.desc())
	return render_template('entry.html', title='Entries', form=form, entries=entries)

@app.route('/edit_entry/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
	form = EntryForm()
	entry = Entry.query.filter_by(id=id).first()
	if form.validate_on_submit():
		entry.good = form.good.data
		entry.bad = form.bad.data
		db.session.add(entry)
		db.session.commit()
		return redirect(url_for('entry'))
	form.good.data = entry.good
	form.bad.data = entry.bad
	return render_template('edit_entry.html', title='Edit Entry', form=form)

@app.route('/del_entry/<int:id>')
@login_required
def del_entry(id):
	try:
		entry = Entry.query.filter_by(id=id).first()
		db.session.delete(entry)
		db.session.commit()
		return redirect(url_for('entry'))
	except:
		return redirect(url_for('entry'))


@app.route('/hbentry', methods=['GET', 'POST'])
@login_required
def hbentry():
	form = HBEntryForm()
	form.hobby_id.choices = [(h.id, h.hobby) for h in Hobby.query.order_by('hobby')]
	if form.validate_on_submit():
		hbentry = HBEntry(
			hb_id=form.hobby_id.data,
			good=form.good.data,
			bad=form.bad.data)
		db.session.add(hbentry)
		db.session.commit()
		return redirect(url_for('hbentry'))
	hbentries = HBEntry.query.order_by(HBEntry.id.desc())
	return render_template('hbentry.html', title='Hobby Entry', form=form, hbentries=hbentries)


@app.route('/edit_hbentry/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_hbentry(id):
	form = HBEntryForm()
	form.hobby_id.choices = [(h.id, h.hobby) for h in Hobby.query.order_by('hobby')]
	hbentry = HBEntry.query.filter_by(id=id).first()
	form.hobby_id.choices.insert(0, (hbentry.hb_id, hbentry.hobby.hobby))
	if form.validate_on_submit():
		hbentry.hb_id = form.hobby_id.data
		hbentry.good = form.good.data
		hbentry.bad = form.bad.data
		db.session.add(hbentry)
		db.session.commit()
		return redirect(url_for('hbentry'))
	form.good.data = hbentry.good
	form.bad.data = hbentry.bad
	return render_template('edit_hbentry.html', title='Edit Hobby Entry', form=form)


@app.route('/del_hbentry/<int:id>')
@login_required
def del_hbentry(id):
	try:
		hbentry = HBEntry.query.filter_by(id=id).first()
		db.session.delete(hbentry)
		db.session.commit()
		return redirect(url_for('hbentry'))
	except:
		return redirect(url_for('hbentry'))


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


@app.route('/del_user/<int:id>')
@login_required
def del_user(id):
	try:
		user = User.query.filter_by(id=id).first()
		db.session.delete(user)
		db.session.commit()
		return redirect(url_for('user'))
	except:
		return redirect(url_for('user'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('admin'))
	form = RegisterForm()
	if form.validate_on_submit():
		username = form.username.data
		email = form.email.data.lower()
		password = form.password.data
		u = User(
			username=username, 
			email=email, 
			password=password)
		db.session.add(u)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)
	

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('admin'))
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data.lower()
		user = User.query.filter_by(email=email).first()
		print email, user
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