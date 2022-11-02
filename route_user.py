import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime

import satori
import satori_auth
import satori_dataset
import satori_dataset_policy
import satori_data_access_permission
import satori_datastore

satori_user = Blueprint('satoriuser', __name__)

@satori_user.route('/satori/user/<action>', methods=['GET'])
def satori_add_or_remove_user(action):

    print("attempting SATORI ACTION: " + action + " user")

    if action == 'add':

        if (request.args.get('apikey') == satori.apikey and 
            request.args.get('duration') is not None and 
            request.args.get('dataset') is not None and 
            request.args.get('email') is not None and
            request.args.get('security_policy_id') is not None
            ):

            dataset_name        = request.args.get('dataset')
            this_email          = request.args.get('email')
            duration            = request.args.get('duration')
            satori_expiration   = datetime.datetime.utcnow() + datetime.timedelta(hours=int(float(duration))) 
            security_policy_id  = request.args.get('security_policy_id')

            # authenticate to Satori for a bearer token
            satori_token = satori_auth.satori_auth()
            # find our dataset
            dataset_id = satori_dataset.get_dataset_id_by_name(satori_token, dataset_name)
            # get overall data policy ID for the dataset
            data_policy_id = satori_dataset_policy.get_dataset_policy_id(satori_token, dataset_id)

            response = satori_data_access_permission.add_user(satori_token, data_policy_id, this_email, satori_expiration, security_policy_id)
            
            if response.status_code == 409:
            
                return "user already existed on this dataset"
            else:            
                # collect the datastores for this dataset as a dictionary
                datastore_connection_info = satori_datastore.get_datastores_from_dataset_id(satori_token, dataset_id)
                datastores = {}

                for item in datastore_connection_info.json()['includeLocations']:
                    datastores.update(satori_datastore.get_one_datastore_connection(satori_token, item['dataStoreId']))

                return render_template('result_adduser.html', result = datastores)
        else:
            return "error: missing or invalid info, required info is: 1) api key, 2) name of Satori Dataset, 3) duration, 4) email"

    elif action == 'remove':

        if (request.args.get('apikey') == satori.apikey and 
            request.args.get('dataset') is not None and 
            request.args.get('email') is not None
            ):

            dataset_name        = request.args.get('dataset')
            this_email          = request.args.get('email')

            # authenticate to Satori for a bearer token
            satori_token = satori_auth.satori_auth()
            # find our dataset
            dataset_id = satori_dataset.get_dataset_id_by_name(satori_token, dataset_name)
            # get overall data policy ID for the dataset
            data_policy_id = satori_dataset_policy.get_dataset_policy_id(satori_token, dataset_id)
            # get the ID of our user that we want to remove from this data policy
            access_id_to_remove = satori_data_access_permission.find_access_id_to_remove_by_email(satori_token, data_policy_id, this_email)
            # remove access by ID
            removal = requests.Response()
            if access_id_to_remove != "-1":
                removal = satori_data_access_permission.remove_access_id(satori_token, access_id_to_remove)

            return render_template('result_removeuser.html', result = removal)
 
        else:
            return "error: missing or invalid info, required info is: 1) api key, 2) name of Satori Dataset, 3) duration, 4) email"                

    else:
        return "incorrect path"