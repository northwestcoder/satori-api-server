import json
import requests
import satori
import satori_common

def get_taxonomy(headers):

	url = "https://{}/api/v1/taxonomy/satori".format(satori.apihost)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("could not find taxonomy: ", err)
		print("Exception TYPE:", type(err))
	else:
		print("retrieved taxonomy") if satori.logging else None
		return response.json()

def get_custom_taxonomy(headers):

	url = "https://{}/api/v1/taxonomy/custom?accountId={}".format(satori.apihost, satori.account_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("could not find taxonomy: ", err)
		print("Exception TYPE:", type(err))
	else:
		print("retrieved taxonomy") if satori.logging else None
		return response.json()
