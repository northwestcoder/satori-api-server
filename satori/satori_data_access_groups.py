import json
import requests

from satori import satori
from satori import satori_common

def get_group_id_by_name(headers, group_name):

	group_search = requests.utils.quote(group_name)
	url = "https://{}/api/v1/directory/group?accountId={}&pageSize=100&search={}".format(satori.apihost, satori.account_id, group_search)
	print("trying to find group id by name: " + url) if satori.logging else None

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		# If multiple groups found, let's return the first one. Make sure your external app is specific enough here.
		group_id = response.json()['records'][0]['id']
		print("group id by name: " + group_id) if satori.logging else None
		return group_id

def add_group(headers, data_policy_id, group_id, expiration, security_policy_id):

	payload = {}
	url = "https://{}/api/v1/data-access-rule/instant-access?AccountId={}&parentId={}".format(satori.apihost, satori.account_id, data_policy_id)
	print("trying to add group: " + url) if satori.logging else None

	payload = json.dumps(
			{
			  "accessLevel": "READ_ONLY",
			  "timeLimit": {
				"shouldExpire": True,
				"expiration": str(expiration.isoformat())
			  },
			  "unusedTimeLimit": {
				"unusedDaysUntilRevocation": 3,
				"shouldRevoke": True
			  },
			  "securityPolicyIds": [
				security_policy_id
			  ],
			  "identity": {
				"identityType": "GROUP",
				"identity": group_id
			  }
			})

	try:
		response = requests.post(url, headers=headers, data=payload)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))		
		return response
	else:
		print("GROUP ADDED, response: " + str(response.text)) if satori.logging else None
		return response

def find_access_id_to_remove_group(headers, data_policy_id, groupname):

	payload = {}
	url = "https://{}/api/v1/data-access-permission?parentId={}&search={}".format(satori.apihost, data_policy_id, groupname)
	print("trying to find access id for existing group: " + url) if satori.logging else None

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		if response.json()['count'] > 0:
			print("access id for existing group: " + response.json()['records'][0]['id']) if satori.logging else None
			return response.json()['records'][0]['id']
		else:
			return "-1"

def remove_group(headers, group_id):

	payload = {}
	url = "https://{}/api/v1/data-access-rule/instant-access/{}".format(satori.apihost, group_id)
	print("trying to remove existing group: " + url) if satori.logging else None

	try:
		response = requests.delete(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
		return response
	else:
		print("remove existing group: " + str(response.text)) if satori.logging else None
		return response

