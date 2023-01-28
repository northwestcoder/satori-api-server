import json
import requests
import time

import satori
import satori_common

def check_token():

	headers = {}
	
	# Authenticate to Satori for a bearer token every hour, else use cache
	if time.time() - satori_common.satori_token[1] > 3600:
		print("refreshing bearer token")
		satori_common.satori_token = satori_common.satori_auth()
		satori_token = satori_common.satori_token
	else:
		print("using cached bearer token")
		satori_token = satori_common.satori_token[0]
	headers = {'Authorization': 'Bearer {}'.format(satori_token), 'Content-Type': 'application/json', 'Accept': 'application/json'}

	return headers