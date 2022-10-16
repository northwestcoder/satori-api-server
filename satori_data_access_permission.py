import satori
import json
import requests

def add_user(satori_token, data_policy_id, email, expiration):

    payload = {}
    headers = {
        'Authorization': 'Bearer {}'.format(satori_token),
        'Content-Type': 'application/json'
        }
        
    accessurl = "https://{}/api/v1/data-access-permission?parentId={}".format(satori.apihost, data_policy_id)

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
                satori.security_policy_id
              ],
              "identity": {
                "identityType": "USER",
                "identity": email
              }
            })

    try:
        response = requests.post(accessurl, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("assignment for dataset failed, is your dataset name valid? :", err)
        print("Exception TYPE:", type(err))
    else:
        return response.json()


def find_access_id_to_remove_by_email(satori_token, data_policy_id, email):

    payload = {}
    headers = {
        'Authorization': 'Bearer {}'.format(satori_token),
        'Content-Type': 'application/json'
        }


    removal_url = "https://{}/api/v1/data-access-permission?parentId={}&search={}".format(satori.apihost, data_policy_id, email)

    try:
        response = requests.get(removal_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("removal of assignment for dataset failed, is your user email valid? :", err)
        print("Exception TYPE:", type(err))
    else:
        return response.json()['records'][0]['id']



def remove_access_id(satori_token, access_id):

    payload = {}
    headers = {
        'Authorization': 'Bearer {}'.format(satori_token),
        'Content-Type': 'application/json'
        }


    removal_by_id_url = "https://{}/api/v1/data-access-permission/{}".format(satori.apihost, access_id)

    try:
        response = requests.delete(removal_by_id_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("removal of access ID for dataset failed, is your user email or access ID valid? :", err)
        print("Exception TYPE:", type(err))
    else:
        print(response.text)
        return response.text
