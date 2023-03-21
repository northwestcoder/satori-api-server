import json
import requests

from satori import satori
from satori import satori_common

def add_user(headers, data_policy_id, email, expiration, security_policy_id):

	payload = {}
	url = "https://{}/api/v1/data-access-rule/instant-access?AccountId={}&parentId={}".format(satori.apihost, satori.account_id, data_policy_id)

	payload = json.dumps(
				{
				"accessLevel": "READ_ONLY",
				"timeLimit": {
					"shouldExpire": "true",
					"expiration": str(expiration.isoformat())
				},
				"unusedTimeLimit": {
					"unusedDaysUntilRevocation": 1,
					"shouldRevoke": "true"
				},
				"securityPolicyIds": [
					security_policy_id
				],
				"identity": {
					"identity": email,
					"identityType": "USER"
					}
				}
			)

	try:
		response = requests.post(url, headers=headers, data=payload)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
		return response
	else:
		print("USER ADDED, response: " + str(response.text)) if satori.logging else None
		return response


def find_access_id_to_remove_by_email(headers, data_policy_id, email):

	payload = {}
	url = "https://{}/api/v1/data-access-permission?parentId={}&search={}".format(satori.apihost, data_policy_id, email)

	try:
		response = requests.get(url, headers=headers)
		print(response.text)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		if response.json()['count'] > 0:
			return response.json()['records'][0]['id']
		else:
			return "-1"

def remove_access_id(headers, access_id):

	payload = {}
	url = "https://{}/api/v1/data-access-rule/instant-access/{}".format(satori.apihost, access_id)

	try:
		response = requests.delete(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
		return response
	else:
		print("response code: " + str(response.status_code))
		return response.text



