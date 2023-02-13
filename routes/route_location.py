import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime
import time

from satori import satori
from satori import satori_common
from satori import satori_bearer_token
from satori import satori_errors as error
from satori import satori_location as location

satori_location = Blueprint('satorilocation', __name__)

@satori_location.route('/satori/location/get_tags_by_datastore', methods=['GET'])
def satori_query_locations_by_datastore():

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):
		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()
		if None != request.args.get('datastore_id'):
			datastore_id = request.args.get('datastore_id')
			print("attempting to find locations for datastore_id " + datastore_id) if satori.logging else None
			response = location.get_all_locations_by_datastore(headers, datastore_id)
			return response.json()
		else:
			return error.USER_PARAMS_MISSING
	else:
		return error.INVALID_APIKEY


@satori_location.route('/satori/location/get_tags_by_table', methods=['GET'])
def satori_query_locations_by_table():

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):
		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()
		if None not in (request.args.get('datastore_id'), request.args.get('database'), request.args.get('schema'), request.args.get('table')):
			datastore_id = request.args.get('datastore_id')
			database = request.args.get('database')
			schema = request.args.get('schema')
			table = request.args.get('table')
			print("attempting to find locations for full table location") if satori.logging else None
			response = location.get_all_tags_for_location_table(headers, datastore_id, database, schema, table)
			return response.json()
		else:
			return error.USER_PARAMS_MISSING
	else:
		return error.INVALID_APIKEY


@satori_location.route('/satori/location/remove_tags_by_table', methods=['GET'])
def satori_remove_tags_for_table():

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):
		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()
		if None not in (request.args.get('datastore_id'), request.args.get('database'), request.args.get('schema'), request.args.get('table')):
			datastore_id = request.args.get('datastore_id')
			database = request.args.get('database')
			schema = request.args.get('schema')
			table = request.args.get('table')
			print("attempting to find locations for full table location") if satori.logging else None
			response = location.get_all_tags_for_location_table(headers, datastore_id, database, schema, table)

			for item in response.json()['records']:
				for tag in item['tags']:
					removal = location.remove_tag_for_location_id(headers, item['id'], tag['name'])

			return "removed all tags from " + database + "." + schema + "." + table
		else:
			return error.USER_PARAMS_MISSING
	else:
		return error.INVALID_APIKEY