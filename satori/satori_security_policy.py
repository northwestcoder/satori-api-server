import json
import requests

from satori import satori
from satori import satori_common

def get_security_policies(headers):

	url = "https://{}/api/v1/security-policies?accountId={}".format(satori.apihost, satori.account_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved " + str(response.json()['count']) + " security policies") if satori.logging else None
		return response.json()