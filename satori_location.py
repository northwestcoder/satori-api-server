import json
import requests
import satori
import satori_common

def get_locations_by_datastore(headers, datastore_id):

	url = "https://{}/api/locations/search?pageSize=5000&dataStoreId={}".format(satori.apihost, datastore_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved location data") if satori.logging else None
		return response.json()


def query_locations_by_datastore(headers, datastore_id):

	url = "https://{}/api/locations/{}/query?pageSize=5000&dataStoreId={}".format(satori.apihost, satori.account_id, datastore_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved location data") if satori.logging else None
		return response.json()