import json
import requests
import satori
import satori_common

def get_all_locations(headers, datastore_id):

	url = "https://{}/api/locations/search?pageSize=2000&dataStoreId={}".format(satori.apihost, satori.datastore_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved location data") if satori.logging else None
		return response.json()