import json
import requests
import satori
import satori_common

def get_security_policies(headers):

	url = "https://{}/api/v1/security-policies?accountId={}".format(satori.apihost, satori.account_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("could not find security policies: ", err)
		print("Exception TYPE:", type(err))
	else:
		print("retrieved " + str(response.json()['count']) + " security policies") if satori.logging else None
		return response.json()