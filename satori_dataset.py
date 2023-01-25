import satori
import json
import requests
import satori_common

def get_dataset_id_by_name(headers, dataset_name):

	url = "https://{}/api/v1/dataset?accountId={}&search={}".format(satori.apihost, satori.account_id, dataset_name)
	print("trying to find dataset id by name: " + url) if satori.logging else None

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("could not find data policy for this dataset: ", err)
		print("Exception TYPE:", type(err))
	else:
		dataset_id = response.json()['records'][0]['id']
		print("dataset id: " + dataset_id) if satori.logging else None
		return dataset_id


def get_all_datasets(headers):

	url = "https://{}/api/v1/dataset?accountId={}&pageSize=1000".format(satori.apihost, satori.account_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("could not find datasets: ", err)
		print("Exception TYPE:", type(err))
	else:
		print("retrieved datasets") if satori.logging else None
		return response.json()
