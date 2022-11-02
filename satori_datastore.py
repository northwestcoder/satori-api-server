import satori
import json
import requests


def get_datastores_from_dataset_id(satori_token, dataset_id):
	headers = {'Authorization': 'Bearer {}'.format(satori_token), 'Content-Type': 'application/json'}
	datastores_url =  "https://{}/api/v1/dataset/{}".format(satori.apihost, dataset_id)

	try:
		#print(datastores_url)
		datastores_response = requests.get(datastores_url, headers=headers)
		datastores_response.raise_for_status()
	except requests.exceptions.RequestException as err:
		#print(datastores_url)
		print("could not find data stores for this dataset: ", err)
		print("Exception TYPE:", type(err))
	else:
		return datastores_response



def get_one_datastore_connection(satori_token, datastore_id):

	#gets a pretty string for a future dictionary, with name, type, hostname, and port 

	headers = {'Authorization': 'Bearer {}'.format(satori_token), 'Content-Type': 'application/json'}
	datastore_url =  "https://{}/api/v1/datastore/{}".format(satori.apihost, datastore_id)

	try:
		#print(datastore_url)
		datastore_response = requests.get(datastore_url, headers=headers)
		datastore_response.raise_for_status()
	except requests.exceptions.RequestException as err:
		#print(datastore_url)
		print("could not find data store with this ID: ", err)
		print("Exception TYPE:", type(err))
		return datastore_response
	else:

		name_and_type = datastore_response.json()['name'] + " (" + datastore_response.json()['type'] + ")"
		host_and_port = datastore_response.json()['satoriHostname'] + ":" + str(datastore_response.json()['originPort'])

		return {name_and_type : host_and_port}
