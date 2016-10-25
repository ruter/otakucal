# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)


class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])


class HobbyForm(FlaskForm):
	hobby = StringField('Hobby', validators=[DataRequired()])


class EntryForm(FlaskForm):
	good = StringField('Good')
	bad = StringField('Bad')


class HBEntryForm(FlaskForm):
	good = StringField('Good')
	bad = StringField('Bad')
	hobby_id = SelectField('Hobby', coerce=int)
		