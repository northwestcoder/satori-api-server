import satori
import json
import requests
import satori_common

def get_datastores_from_dataset_id(headers, dataset_id):

	url =  "https://{}/api/v1/dataset/{}".format(satori.apihost, dataset_id)
	print("trying to find datastores in this dataset: " + url) if satori.logging else None

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		return response

def get_one_datastore_connection(headers, datastore_id):

	#gets a pretty string for a future dictionary, with name, type, hostname, and port 
	url =  "https://{}/api/v1/datastore/{}".format(satori.apihost, datastore_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
		return response
	else:

		name_and_type = response.json()['name'] + " (" + response.json()['type'] + ")"
		host_and_port = response.json()['satoriHostname'] + ":" + str(response.json()['originPort'])

		return {name_and_type : host_and_port}

def get_all_datastores(headers):

	url =  "https://{}/api/v1/datastore?accountId={}&pageSize=500".format(satori.apihost, satori.account_id)
	print("trying to find all datastores: " + url) if satori.logging else None

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		return response.json()