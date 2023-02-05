import json
import requests

from satori import satori
from satori import satori_common

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


def get_one_datastore(headers, datastore_id):

	url =  "https://{}/api/v1/datastore/{}".format(satori.apihost, datastore_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
		return response
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

    
def get_datastore_locations(headers, datastore_id):

    url = "https://{}/api/locations/{}/query?pageSize=1000&dataStoreId={}".format(satori.apihost, satori.account_id, datastore_id)

    try:
        source_datastore_location_response = requests.get(url, headers=headers)
        source_datastore_location_response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("could not find datastores locations: ", err)
        print("Exception TYPE:", type(err))
    else:
        return source_datastore_location_response
    

def update_datastore_locations(headers, location_id, tag_id):

    url = "https://app.satoricyber.com/api/locations/{}".format(location_id)

    try:
        update_tags_response = requests.put(url, headers=headers, data='{"addTags": ["' + tag_id + '"], "removeTags": [], "notes": "Updated via Satori Copy Inventory API"}')
        update_tags_response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("could not update datastore locations: ", err)
        print("Exception TYPE:", type(err))
    else:
        return update_tags_response    