import satori
import json
import requests

# Authenticate to Satori for a bearer token

def satori_auth():
	authheaders = {'content-type': 'application/json','accept': 'application/json'}
	url = "https://{}/api/authentication/token".format(satori.host)
	try:
	    r = requests.post(url, 
	                      headers=authheaders, 
	                      data='{"serviceAccountId": "' + satori.serviceaccount_id + 
	                      '", "serviceAccountKey": "' + satori.serviceaccount_key + '"}')
	    response = r.json()
	    satori_token = response["token"]
	except Exception as err:
	    print("Bearer Token Failure: :", err)
	    print("Exception TYPE:", type(err))
	else:
		return satori_token