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