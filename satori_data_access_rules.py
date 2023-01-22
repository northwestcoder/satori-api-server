import satori
import json
import requests
import satori_common


def get_access_rules_for_data_policy(headers, data_policy_id):
	return True


def add_user_access_rule(headers, data_policy_id, email, expiration, security_policy_id):

    payload = {}
    url = "https://{}/api/data-access-request/submit-request?AccountId={}&dataPolicyId={}".format(satori.apihost, satori.account_id, data_policy_id)

    payload = json.dumps(
                {
                "dataAccessRuleId":"71f24aef-e5b3-4b91-8010-f2fba736c15e",
                "message":"ok ok ok "
                }
            )

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("assignment for dataset failed, is your dataset name valid? :", err)
        print("Exception TYPE:", type(err))
        return response
    else:
        print(response.status_code)
        return response

