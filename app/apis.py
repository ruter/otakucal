# -*- coding: utf-8 -*-

from . import api, app
from flask_restful import Resource, reqparse
from .models import User, Entry, Hobby, HBEntry

from flask import json, make_response
import random
from datetime import datetime
from itertools import chain

HBENTRY_MAX = HBEntry.query.count()

@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps({'error': 'Not found'}), 404)


def get_entry_list():
	random.seed(datetime.utcnow())
	entry_id_list = random.sample(range(1, Entry.query.count() + 1), 3)
	good_id = entry_id_list[:2]
	bad_id = entry_id_list[-1]
	entries = {}
	good_list = Entry.query.with_entities(Entry.good).filter(Entry.id.in_(good_id)).all()
	entries['good'] = [good.good for good in good_list]
	entries['bad'] = Entry.query.with_entities(Entry.bad).filter_by(id=bad_id).first().bad
	# return json.dumps(entries, ensure_ascii=False).decode('utf-8')
	return entries


class Entries(Resource):
	def get(self):
		return make_response(
			json.dumps({'result': get_entry_list()}, ensure_ascii=False).decode('utf-8'))


class Hobbies(Resource):
	def get(self):
		hobbies = {'hobbies': [hb.hobby for hb in Hobby.query.with_entities(Hobby.hobby).all()]}
		return make_response(
			json.dumps({'result': hobbies}, ensure_ascii=False).decode('utf-8'))


class HBEntry(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('hobby', action='append')
		args = parser.parse_args()
		hobbies = args['hobby']
		hbentries = {}
		good = []
		bad = []
		for hb in hobbies:
			hobby = Hobby.query.filter_by(hobby=hb).first()
			good.extend([h.good for h in hobby.hb_entries])
			bad.extend([h.bad for h in hobby.hb_entries])
		hbentries['hobby_entries'] = {'good': good, 'bad': bad}

		return make_response(json.dumps({'result': hbentries}, ensure_ascii=False).decode('utf-8'))
		

api.add_resource(Hobbies, '/otakucal/v1.0/hobbies', endpoint='hobbies')
api.add_resource(Entries, '/otakucal/v1.0/entries', endpoint='entries')
api.add_resource(HBEntry, '/otakucal/v1.0/hb_entries', endpoint='hb_entries')
