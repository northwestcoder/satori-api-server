import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime
import time

from satori import satori
from satori import satori_common
from satori import satori_bearer_token
from satori import satori_errors as error
from satori import satori_location
from satori import satori_taxonomy

from collibra import update_satori
from collibra import collibra_token


satori_collibra = Blueprint('satoricollibra', __name__)

@satori_collibra.route('/collibra/update_satori', methods=['GET'])
def collibra_actions():

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):
		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()

		if None not in (request.args.get('datastore_id'), request.args.get('database'), request.args.get('schema'), request.args.get('table')):
			datastore_id = request.args.get('datastore_id')
			database = request.args.get('database')
			schema = request.args.get('schema')
			table = request.args.get('table')
			print("attempting to update satori from collibra") if satori.logging else None

			coll_token = collibra_token.collibra_auth()
			

			# Check for additions from Collibra to then update Satori
			coll_headers = {
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
			'content-type': 'application/json',
			'accept': 'application/json',
			'csrfToken': coll_token['collibra_token'],
			'Cookie': "JSESSIONID={}".format(coll_token['collibra_session_id'])
			}

			collibra_url = "https://satoricyber.collibra.com/rest/2.0/assets"
			r = requests.get(collibra_url, headers=coll_headers)

			assets = r.json()

			for asset in assets["results"]:

				# this next line is a sloppy match, we need to do a cleaner Collibra search here
				if table.upper() in (asset["name"].upper()):

					asset_id = asset["id"]
					column_name = asset["displayName"]

					url = "https://satoricyber.collibra.com/rest/2.0/assets/{}/tags".format(asset_id)
					r = requests.get(url, headers=coll_headers)
					tags_json = r.json()

					if len(tags_json) > 0:
						for tag in tags_json:
							tag_to_add = tag["name"]
							print("Adding tag {} for column {}".format(tag_to_add, column_name))
							search = database + "." + schema + "." + table
							update_satori.add_tag_to_satori(headers, datastore_id, search, column_name, tag_to_add)

			result = {}
			result['location:'] = search

			return render_template('result_collibra.html', result = result)

			#return "updated location " + search + " with relevant Collibra Tags"


		else:
			return error.USER_PARAMS_MISSING

	else:
		return error.INVALID_APIKEY
