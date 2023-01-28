import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime
import time

import satori
import satori_common
import satori_bearer_token
import satori_errors as error
import satori_location as location

satori_location = Blueprint('satorilocation', __name__)

@satori_location.route('/satori/location/get_locations_by_datastore', methods=['GET'])
def satori_get_locations_by_datastore():

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):
		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()
		if None != request.args.get('datastore_id'):
			datastore_id = request.args.get('datastore_id')
			print("attempting to find locations for datastore_id " + datastore_id) if satori.logging else None
			response = location.get_locations_by_datastore(headers, datastore_id)
			return response
		else:
			return error.USER_PARAMS_MISSING
	else:
		return error.INVALID_APIKEY


@satori_location.route('/satori/location/get_tags_by_datastore', methods=['GET'])
def satori_query_locations_by_datastore():

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):
		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()
		if None != request.args.get('datastore_id'):
			datastore_id = request.args.get('datastore_id')
			print("attempting to find locations for datastore_id " + datastore_id) if satori.logging else None
			response = location.query_locations_by_datastore(headers, datastore_id)
			return response
		else:
			return error.USER_PARAMS_MISSING
	else:
		return error.INVALID_APIKEY