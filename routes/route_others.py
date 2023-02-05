import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime
import time

from satori import satori
from satori import satori_common
from satori import satori_bearer_token
from satori import satori_errors as error
from satori import satori_security_policy
from satori import satori_datastore
from satori import satori_dataset
from satori import satori_taxonomy
from satori import satori_dac
from satori import satori_masking_profile

satori_others = Blueprint('satoriothers', __name__)

@satori_others.route('/satori/other/<action>', methods=['GET'])
def satori_get_others(action):

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):

		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()

		if action == 'security_policies':
			print("attempting to retrieve security policies") if satori.logging else None
			response = satori_security_policy.get_security_policies(headers)
			return response
		elif action == 'datastores':
			print("attempting to retrieve datastores") if satori.logging else None
			response = satori_datastore.get_all_datastores(headers)
			return response
		elif action == 'taxonomy':
			print("attempting to retrieve taxonomy") if satori.logging else None
			response = satori_taxonomy.get_all_satori_taxonomy(headers)
			return response
		elif action == 'custom_taxonomy':
			print("attempting to retrieve custom taxonomy") if satori.logging else None
			response = satori_taxonomy.get_all_custom_taxonomy(headers)
			return response
		elif action == 'data_access_controllers':
			print("attempting to retrieve dacs") if satori.logging else None
			response = satori_dac.get_data_access_controllers(headers)
			return response
		elif action == 'datasets':
			print("attempting to retrieve datasets") if satori.logging else None
			response = satori_dataset.get_all_datasets(headers)
			return response
		elif action == 'masking':
			print("attempting to retrieve masking") if satori.logging else None
			response = satori_masking_profile.get_all_masking_profiles(headers)
			return response

		else:
			return error.BAD_PATH

	else:
		return error.INVALID_APIKEY

@satori_others.route('/satori/datastore', methods=['GET'])
def satori_get_one_datastore():

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):

		if request.args.get('datastore_id') is not None:

			# Authenticate to Satori for a bearer token every hour, else use cache
			headers = satori_bearer_token.check_token()

			print("attempting to retrieve security policies") if satori.logging else None
			response = satori_datastore.get_one_datastore(headers, request.args.get('datastore_id'))
			return response.json()

		else:
			return error.USER_PARAMS_MISSING

	else:
		return error.INVALID_APIKEY

