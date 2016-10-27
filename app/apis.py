# -*- coding: utf-8 -*-

from . import api
from flask_restful import Resource
from .models import User, Entry, Hobby, HBEntry

#ENDPOINT = 'https://api.example.com/v1/'

class DefaultEntries(Resource):
	def get(self):
		return {'Entry': 'Happy'}


# class EntryList(Resource):
# 	def get(self, page=1, num=)
		

api.add_resource(DefaultEntries, '/otakucal/v1/entries', endpoint='default')
