import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime
import time

from satori import satori
from satori import satori_common
from satori import satori_bearer_token as token
from satori import satori_errors as error
from satori import satori_dataset
from satori import satori_dataset_policy
from satori import satori_datastore
from satori import satori_data_access_users
from satori import satori_data_access_groups

satori_group = Blueprint('satorigroup', __name__)

@satori_group.route('/satori/group/<action>', methods=['GET'])
def satori_add_or_remove_group(action):

	print("attempting SATORI ACTION: " + action + " group") if satori.logging else None

	# TODO: we currenty have a placeholder "api key" hardwired into this code example (in satori.py)
	# TODO: instead, we should call into a GCP or AWS secrets manager to retrieve a key that we have predefined.
	# TODO: https://cloud.google.com/secret-manager/docs/reference/rest or
	# TODO: https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-python.html

	# we look for the API key in the URL params, or in the https header
	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):

		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = token.check_token()

		if action == 'add':

			if (None not in ( 
				request.args.get('duration'), 
				request.args.get('dataset'), 
				request.args.get('groupname'), 
				request.args.get('security_policy_id'))):

				duration            = request.args.get('duration')
				dataset_name        = request.args.get('dataset')
				groupname           = request.args.get('groupname')
				security_policy_id  = request.args.get('security_policy_id')
				satori_expiration   = datetime.datetime.utcnow() + datetime.timedelta(hours=int(float(duration))) 

				# find our dataset
				dataset_id = satori_dataset.get_dataset_id_by_name(headers, dataset_name)
				# get overall data policy ID for the dataset
				data_policy_id = satori_dataset_policy.get_dataset_policy_id(headers, dataset_id)

				# get group ID by name
				group_id = satori_data_access_groups.get_group_id_by_name(headers, groupname)

				#add group ID to access list for the dataset				
				response = satori_data_access_groups.add_group(headers, data_policy_id, group_id, satori_expiration, security_policy_id)
				
				if response.status_code == 409:
					return error.USER_EXISTS
				else:            
					# collect the datastores for this dataset as a dictionary
					datastore_connection_info = satori_datastore.get_datastores_from_dataset_id(headers, dataset_id)
					datastores = {}

					for item in datastore_connection_info.json()['includeLocations']:
						datastores.update(satori_datastore.get_one_datastore_connection(headers, item['dataStoreId']))

					return render_template('result_adduser.html', result = datastores)
			else:
				return error.USER_PARAMS_MISSING

		elif action == 'remove':

			if (None not in (
				request.args.get('dataset'), 
				request.args.get('groupname'))):

				dataset_name       = request.args.get('dataset')
				groupname          = request.args.get('groupname')

				# find our dataset
				dataset_id = satori_dataset.get_dataset_id_by_name(headers, dataset_name)
				# get overall data policy ID for the dataset
				data_policy_id = satori_dataset_policy.get_dataset_policy_id(headers, dataset_id)
				# get the ID of our group that we want to remove from this data policy
				group_id = satori_data_access_groups.get_group_id_by_name(headers, groupname)

				group_access_id = satori_data_access_groups.find_access_id_to_remove_group(headers, data_policy_id, group_id)

				# remove access by ID
				removal = requests.Response()
				if group_id != "-1":
					removal = satori_data_access_groups.remove_group(headers, group_access_id)

				return render_template('result_removeuser.html', result = removal)
	 
			else:
				return error.USER_PARAMS_MISSING
		else:
			return error.BAD_PATH
	else:
		return error.INVALID_APIKEY