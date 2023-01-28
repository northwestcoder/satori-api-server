import json
import requests

from satori import satori
from satori import satori_common

def get_dataset_policy_id(headers, dataset_id):

	url =  "https://{}/api/v1/dataset/{}".format(satori.apihost, dataset_id)
	print("trying to find dataset policy id: " + url) if satori.logging else None

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		dataset_policy_id = response.json()['dataPolicyId']
		print("dataset policy id: " + dataset_policy_id) if satori.logging else None
		return dataset_policy_id