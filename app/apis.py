# -*- coding: utf-8 -*-

from . import api, app
from flask_restful import Resource, reqparse
from .models import User, Entry, Hobby, HBEntry

from flask import json, make_response
import random
from datetime import datetime
from itertools import chain


@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps({'error': 'Not found'}), 404)

def rand_result(rand_num, num):
	random.seed(datetime.utcnow())
	rs = random.sample(range(1, rand_num + 1), num)
	return rs

def get_entries(rand_num, num, max_num):
	entry_id_list = rand_result(rand_num, num)
	good_id = entry_id_list[:max_num]
	bad_id = entry_id_list[max_num:]
	entries = {}
	good_list = Entry.query.with_entities(Entry.good).filter(Entry.id.in_(good_id)).all()
	entries['good'] = [good.good for good in good_list]
	entries['bad'] = Entry.query.with_entities(Entry.bad).filter_by(id=bad_id).first().bad
	return entries


class Entries(Resource):
	def get(self):
		return make_response(
			json.dumps({'result': get_entries(Entry.query.count(), 3, 2)}, ensure_ascii=False).decode('utf-8'))


class Hobbies(Resource):
	def get(self):
		hobbies = {'hobbies': [hb.hobby for hb in Hobby.query.with_entities(Hobby.hobby).all()]}
		return make_response(
			json.dumps({'result': hobbies}, ensure_ascii=False).decode('utf-8'))


class HBEntry(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('hobby', action='append')
		parser.add_argument('lucky', type=bool)
		args = parser.parse_args()

		hobbies = args['hobby']
		lucky = args['lucky']

		hbentries = {}
		good = []
		bad = []

		if hobbies:
			entry_list = []
			for hb in hobbies:
				hobby = Hobby.query.filter_by(hobby=hb).first()
				entry_list.extend([h for h in hobby.hb_entries])
			
			if len(entry_list) > 9:
				entry_list = random.sample(entry_list, 9)
				good = [e.good for e in entry_list[:6]]
				bad = [e.bad for e in entry_list[6:]]
				rs = get_entries(Entry.query.count(), 3, 2)
				good.extend(rs['good'])
				bad.extend(rs['bad'])
			else:
				e_num = 12 - len(entry_list)
				entry_list = random.sample(entry_list, len(entry_list))
				good = [e.good for e in entry_list[:len(entry_list) / 2]]
				bad = [e.bad for e in entry_list[len(entry_list) / 2:]]
				rs = get_entries(Entry.query.count(), e_num, e_num / 2)
				good.extend(rs['good'])
				bad.extend(rs['bad'])
		else:
			rs = get_entries(Entry.query.count(), 12, 8)
			good.extend(rs['good'])
			bad.extend(rs['bad'])

		if lucky:
			random.seed(datetime.utcnow())
			hbentries['lucky_val'] = str(random.randint(60, 120)) + '%'

		hbentries['hobby_entries'] = {'good': good, 'bad': bad}
		return make_response(json.dumps({'result': hbentries}, ensure_ascii=False).decode('utf-8'))
		

api.add_resource(Hobbies, '/otakucal/v1.0/hobbies', endpoint='hobbies')
api.add_resource(Entries, '/otakucal/v1.0/entries', endpoint='entries')
api.add_resource(HBEntry, '/otakucal/v1.0/hb_entries', endpoint='hb_entries')
