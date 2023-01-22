import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime
import time

import satori
import satori_common
import satori_dataset
import satori_dataset_policy
import satori_datastore
import satori_data_access_users
import satori_data_access_groups

satori_group = Blueprint('satorigroup', __name__)

@satori_group.route('/satori/group/<action>', methods=['GET'])
def satori_add_or_remove_group(action):

    print("attempting SATORI ACTION: " + action + " group") if satori.logging else None

    # Authenticate to Satori for a bearer token every hour, else use cache
    if time.time() - satori_common.satori_token[1] > 3600:
        print("refreshing bearer token")
        satori_common.satori_token = satori_common.satori_auth()
        satori_token = satori_common.satori_token
    else:
        print("using cached bearer token")
        satori_token = satori_common.satori_token[0]
    headers = {'Authorization': 'Bearer {}'.format(satori_token), 'Content-Type': 'application/json'}

# TODO: we currenty have a placeholder "api key" hardwired into this code example (in satori.py)
# TODO: instead, we should call into a GCP or AWS secrets manager to retrieve a key that we have predefined.
# TODO: https://cloud.google.com/secret-manager/docs/reference/rest or
# TODO: https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-python.html

    if action == 'add':

        if (request.args.get('apikey') == satori.apikey and 
            request.args.get('duration') is not None and 
            request.args.get('dataset') is not None and 
            request.args.get('groupname') is not None and
            request.args.get('security_policy_id') is not None
            ):

            dataset_name        = request.args.get('dataset')
            groupname          = request.args.get('groupname')
            duration            = request.args.get('duration')
            satori_expiration   = datetime.datetime.utcnow() + datetime.timedelta(hours=int(float(duration))) 
            security_policy_id  = request.args.get('security_policy_id')

            # find our dataset
            dataset_id = satori_dataset.get_dataset_id_by_name(headers, dataset_name)
            # get overall data policy ID for the dataset
            data_policy_id = satori_dataset_policy.get_dataset_policy_id(headers, dataset_id)

            group_id = satori_data_access_groups.get_group_id_by_name(headers, groupname)
            response = satori_data_access_groups.add_group(headers, data_policy_id, group_id, satori_expiration, security_policy_id)
            
            if response.status_code == 409:
                return "user already existed on this dataset"
            else:            
                # collect the datastores for this dataset as a dictionary
                datastore_connection_info = satori_datastore.get_datastores_from_dataset_id(headers, dataset_id)
                datastores = {}

                for item in datastore_connection_info.json()['includeLocations']:
                    datastores.update(satori_datastore.get_one_datastore_connection(headers, item['dataStoreId']))

                return render_template('result_adduser.html', result = datastores)
        else:
            return "error: missing or invalid info, required info is: 1) api key, 2) name of Satori Dataset, 3) duration, 4) email"

    elif action == 'remove':

        if (request.args.get('apikey') == satori.apikey and 
            request.args.get('dataset') is not None and 
            request.args.get('groupname') is not None
            ):

            dataset_name       = request.args.get('dataset')
            groupname          = request.args.get('groupname')

            # find our dataset
            dataset_id = satori_dataset.get_dataset_id_by_name(headers, dataset_name)
            # get overall data policy ID for the dataset
            data_policy_id = satori_dataset_policy.get_dataset_policy_id(headers, dataset_id)
            # get the ID of our group that we want to remove from this data policy
            group_id = satori_data_access_groups.get_group_id_by_name(headers, groupname)
            group_access_id = satori_data_access_groups.find_access_id_to_remove_group(headers, data_policy_id, group_id)

            # remove access by ID
            removal = requests.Response()
            if group_id != "-1":
                removal = satori_data_access_groups.remove_group(headers, group_access_id)

            return render_template('result_removeuser.html', result = removal)
 
        else:
            return "error: missing or invalid info, required info is: 1) api key, 2) name of Satori Dataset, 3) duration, 4) email"                

    else:
        return "incorrect path"