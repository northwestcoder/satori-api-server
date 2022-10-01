import satori
import json
import requests

def get_policy_id_by_name(satori_token, policy_name):
	
	policy_headers = {
    'Authorization': 'Bearer {}'.format(satori_token),
    'Content-Type': 'application/json'
     }

    policy_url =  "https://{}/api/v1/dataset?accountId={}&search={}".format(satori.host, satori.account_id, dataset_name)

    try:
        policy_response = requests.get(policy_url, headers=policy_headers)
        policy_response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("could not find security policy: ", err)
        print("Exception TYPE:", type(err))
    else:
        # more that one policy might have been found, we are retrieving the first one:
        return policy_response.json()['records'][0]['id']