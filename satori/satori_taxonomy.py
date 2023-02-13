import json
import requests
from flask import jsonify, make_response

from satori import satori
from satori import satori_common

def get_all_satori_taxonomy(headers):

	url = "https://{}/api/v1/taxonomy/satori".format(satori.apihost)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved taxonomy") if satori.logging else None
		return response.json()

def get_all_custom_taxonomy(headers):

	url = "https://{}/api/v1/taxonomy/custom?accountId={}".format(satori.apihost, satori.account_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved taxonomy") if satori.logging else None
		return response.json()


def create_taxonomy(headers, body):

	url = "https://{}/api/v1/taxonomy/custom/classifier?accountId={}".format(satori.apihost, satori.account_id)

	payload = json.dumps(body)

	response = requests.post(url, headers=headers, data=payload)
	print("created taxonomy:") if satori.logging else None
	print(response.json()) if satori.logging else None
	return response.json()


def taxonomy_helper(myjson, action, searchkey, result):

	# recursive function on the entire custom taxonomy of the Satori account 

	# "action" is how we will search, e.g. by name, by id, or by tag name
	# "searchKey" is the thing we are searching for
	# "result" is our dictionary that we build, with id, name, tag name, etc
	if type(myjson) == str:
		myjson = json.loads(myjson)
	if type(myjson) is dict:
		for jsonkey in myjson:
			if jsonkey in ("createdAt", "updatedAt", "nameCreatedBy", "nameUpdatedBy", 
				"description", "parentNode", "scope", "config", "name", "id", "tag", "nodeType") and myjson[action] == searchkey:
				result[jsonkey] = myjson[jsonkey]
			if type(myjson[jsonkey]) in (list, dict):
				taxonomy_helper(myjson[jsonkey], action, searchkey, result)
	elif type(myjson) is list:
		for item in myjson:
			if type(item) in (list, dict):
				taxonomy_helper(item, action, searchkey, result)
	return result


def get_one_taxonomy(headers, action, taxonomy_name):

	url = "https://{}/api/v1/taxonomy/custom?accountId={}".format(satori.apihost, satori.account_id)
	print("trying to find info for taxonomy: " + taxonomy_name) if satori.logging else None

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		taxonomies = response.json()
		result = taxonomy_helper(taxonomies, "name", taxonomy_name, {})
		print("taxonomy_info: " + str(result)) if satori.logging else None
		return result

