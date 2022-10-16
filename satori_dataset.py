import satori
import json
import requests

def get_dataset_id_by_name(satori_token, dataset_name):

    dataset_headers = {
        'Authorization': 'Bearer {}'.format(satori_token),
        'Content-Type': 'application/json'
        }

    dataset_url =  "https://{}/api/v1/dataset?accountId={}&search={}".format(satori.apihost, satori.account_id, dataset_name)

    try:
        dataset_response = requests.get(dataset_url, headers=dataset_headers)
        dataset_response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(dataset_url)
        print("could not find data policy for this dataset: ", err)
        print("Exception TYPE:", type(err))
    else:
        return dataset_response.json()['records'][0]['id']