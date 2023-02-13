import json
import requests

from satori import satori
from satori import satori_common

def get_all_locations_by_datastore(headers, datastore_id):

	url = "https://{}/api/locations/{}/query?pageSize=5000&dataStoreId={}".format(satori.apihost, satori.account_id, datastore_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved location data") if satori.logging else None
		return response
		

def get_one_location_by_datastore_and_search(headers, datastore_id, search):

	url = "https://{}/api/locations/{}/query?pageSize=5000&dataStoreId={}&search={}".format(satori.apihost, satori.account_id, datastore_id, search)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved location data") if satori.logging else None
		return response


def get_all_tags_for_location_table(headers, datastore_id, database, schema, table):

	search = database + "." + schema + "." + table
	url = "https://{}/api/locations/{}/query?pageSize=5000&dataStoreId={}&search={}".format(satori.apihost, satori.account_id, datastore_id, search)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved location data for: " + database + "." + schema + "." + table) if satori.logging else None
		return response

def remove_tag_for_location_id(headers, location_id, tagname):

	data='{"addTags": [], "removeTags": ["' + tagname + '"], "notes": "Tag removed by API Relay Server"}'	
	url = "https://{}/api/locations/{}".format(satori.apihost, location_id)

	try:
		print("attempting to remove tag for location id: " + location_id) if satori.logging else None
		response = requests.put(url, headers=headers, data=data)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved location data") if satori.logging else None
		return response