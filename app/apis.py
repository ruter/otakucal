# -*- coding: utf-8 -*-

from . import api
from flask_restful import Resource
from .models import User, Entry, Hobby, HBEntry

import json
import random
from datetime import datetime


ENTRY_MAX = Entry.query.count()
HBENTRY_MAX = HBEntry.query.count()


def get_entry_list():
	random.seed(datetime.utcnow())
	entry_id_list = random.sample(range(1, ENTRY_MAX + 1), 3)
	good_id = entry_id_list[:2]
	bad_id = entry_id_list[-1]
	entries = {}
	good_list = Entry.query.with_entities(Entry.good).filter(Entry.id.in_(good_id)).all()
	entries['good'] = [good.good for good in good_list]
	entries['bad'] = Entry.query.with_entities(Entry.bad).filter_by(id=bad_id).first().bad
	return json.dumps(entries, ensure_ascii=False).encode('utf-8')


class Entries(Resource):
	def get(self):
		return {'result': get_entry_list()}


# class EntryList(Resource):
# 	def get(self, page=1, num=)
		

api.add_resource(Entries, '/otakucal/v1/entries', endpoint='entries')
