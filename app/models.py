# -*- coding: utf-8 -*-

from sqlalchemy.ext.hybrid import hybrid_property

from . import db, bcrypt

from datetime import datetime

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(32), index=True, unique=True)
	email = db.Column(db.String(64), unique=True)
	_password = db.Column(db.String(64))
	reg_time = db.Column(db.DateTime, default=datetime.utcnow)
	last_login = db.Column(db.DateTime)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def _set_password(self, plaintext):
		self._password = bcrypt.generate_password_hash(plaintext)

	def is_correct_password(self, plaintext):
		if bcrypt.check_password_hash(self._password, plaintext):
			return True
		return False

	def __repr__(self):
		return '<User %r>' % self.username


class Entry(db.Model):
	__tablename__ = 'entries'
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	good = db.Column(db.String(64))
	bad = db.Column(db.String(64))

	def __repr__(self):
		return '<Entry %r & %r>' % (self.good, self.bad)


class Hobby(db.Model):
	__tablename__ = 'hobbies'
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	hobby = db.Column(db.String(12))
	hb_entries = db.relationship('HBEntry', backref='hobby', lazy='dynamic')


class HBEntry(db.Model):
	__tablename__ = 'hbentries'
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	hb_id = db.Column(db.Integer, db.ForeignKey('hobbies.id'))
	good = db.Column(db.String(64))
	bad = db.Column(db.String(64))
	
	def __repr__(self):
		return '<Entry %r & %r>' % (self.good, self.bad)

	
		