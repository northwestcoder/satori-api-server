import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime
import time

import satori
import satori_common
import satori_bearer_token
import satori_errors as error
import satori_taxonomy as taxonomy

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