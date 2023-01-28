import json
import requests
import time

from satori import satori

#helper function to get a new bearer token if older than one hour

def satori_auth():

	creation_time = time.time()
	headers = {'content-type': 'application/json', 'accept': 'application/json'}
	url = "https://{}/api/authentication/token".format(satori.apihost)
	try:
		r = requests.post(url, 
						  headers=headers, 
						  data='{"serviceAccountId": "' + satori.serviceaccount_id + 
						  '", "serviceAccountKey": "' + satori.serviceaccount_key + '"}')
		response = r.json()
		satori_token = response["token"]
	except Exception as err:
		print("Exception TYPE:", type(err))
	else:
		print("new token created at: " + str(creation_time)) if satori.logging else None
		print("token: " + str(satori_token)) if satori.logging else None
		return [satori_token, creation_time]

#first token at startup
satori_token = satori_auth()