import requests
import json
from collibra import collibra

collibra_username = collibra.username
collibra_password = collibra.password


def collibra_auth():

	headers = {
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
'content-type': 'application/json',
'accept': 'application/json'}

	url = "https://satoricyber.collibra.com/rest/2.0/auth/sessions"
	print("Authenticating with Collibra...")
	r = requests.post(url, headers=headers, data='{"username": "' + collibra_username + '", "password": "' + collibra_password + '"}')

	collibra_response = {}

	response = r.json()
	csrf_token = response["csrfToken"]
	collibra_response['collibra_token'] = csrf_token
	#print("Got collibra CSRF token {}".format(csrf_token))
	cookies_set = r.headers["Set-Cookie"]
	#print(cookies_set)
	session_id = cookies_set[11:47] # between JSESSIONID and ;
	#print(session_id)
	collibra_response['collibra_session_id'] = session_id
	#print(collibra_response)
	return collibra_response