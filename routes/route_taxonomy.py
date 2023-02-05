import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime
import time

from satori import satori
from satori import satori_common
from satori import satori_bearer_token
from satori import satori_errors as error
from satori import satori_taxonomy as taxonomy
from satori import satori_datastore as datastore


satori_taxonomy = Blueprint('satoritaxonomy', __name__)

@satori_taxonomy.route('/satori/taxonomy/find_by_<action>', methods=['GET'])
def satori_get_taxonomy(action):

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):
		if action in ('name', 'id', 'tag'):
			# Authenticate to Satori for a bearer token every hour, else use cache
			headers = satori_bearer_token.check_token()
			if None != request.args.get('search'):
				search = request.args.get('search')
				print("attempting to find taxonomy using " + action) if satori.logging else None
				response = taxonomy.get_one_taxonomy(headers, action, search)
				return response
			else:
				return error.USER_PARAMS_MISSING
		else:
			return error.BAD_PATH
	else:
		return error.INVALID_APIKEY


@satori_taxonomy.route('/satori/taxonomy/create', methods=['POST'])
def satori_create_taxonomy():

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):
		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()
		print("attempting to create taxonomy") if satori.logging else None
		response = taxonomy.create_taxonomy(headers, request.json)
		return response
	else:
		return error.INVALID_APIKEY



@satori_taxonomy.route('/satori/copy/taxonomy', methods=['GET'])
def satori_copy_taxonomy():


	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):

		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()
		if None not in (request.args.get('source_datastore_id'), request.args.get('target_datastore_id')):
			source_datastore_id = request.args.get('source_datastore_id')
			target_datastore_id = request.args.get('target_datastore_id')
			print("attempting to copy taxonomy") if satori.logging else None

			source_name = datastore.get_one_datastore(headers, source_datastore_id).json()['name']
			target_name = datastore.get_one_datastore(headers, target_datastore_id).json()['name']

			source_locations = datastore.get_datastore_locations(headers, source_datastore_id)
			target_locations = datastore.get_datastore_locations(headers, target_datastore_id)

			tag_response = {"source" : source_name, "target" : target_name}

			for source_item in source_locations.json()['records']:
				schema = source_item['location']['schema']
				table = source_item['location']['table']
				column = source_item['location']['column']
				tags = source_item['tags']
				for target_item in target_locations.json()['records']:
					if schema == target_item['location']['schema'] and \
					table == target_item['location']['table'] and \
					column == target_item['location']['column']:
						target_location_id = target_item['id']
						if tags:
							for tagitem in tags:
								print("updating " + schema + ":" + table + ":" + column + " with tag: " + tagitem['name'])
								datastore.update_datastore_locations(headers, target_location_id, tagitem['name'])
								tag_response[target_location_id] = "updated " + schema + ":" + table + ":" + column + " with tag: " + tagitem['name']

			return tag_response

		else:

			return error.USER_PARAMS_MISSING

	else:

		return error.INVALID_APIKEY



