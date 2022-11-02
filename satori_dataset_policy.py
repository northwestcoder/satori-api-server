import satori
import json
import requests

def get_dataset_policy_id(satori_token, dataset_id):

    headers = {'Authorization': 'Bearer {}'.format(satori_token), 'Content-Type': 'application/json'}
    data_policy_url =  "https://{}/api/v1/dataset/{}".format(satori.apihost, dataset_id)

    try:
        #print(data_policy_url)
        policy_response = requests.get(data_policy_url, headers=headers)
        policy_response.raise_for_status()
    except requests.exceptions.RequestException as err:
        #print(data_policy_url)
        print("could not find data policy for this dataset: ", err)
        print("Exception TYPE:", type(err))
    else:
        return policy_response.json()['dataPolicyId']