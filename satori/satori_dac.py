import json
import requests

from satori import satori
from satori import satori_common

def get_data_access_controllers(headers):

	url = "https://{}/api/v1/data-access-controllers?accountId={}".format(satori.apihost, satori.account_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved taxonomy") if satori.logging else None
		return response.json()