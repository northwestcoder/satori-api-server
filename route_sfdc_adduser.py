import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime

import satori
import satori_auth
import satori_dataset
import satori_dataset_policy
import satori_data_access_permission


sfdc_adduser = Blueprint('adduser', __name__)

@sfdc_adduser.route('/adduser', methods=['GET'])
def adduser():

    if (request.args.get('apikey') == satori.apikey and 
        request.args.get('duration') is not None and 
        request.args.get('dataset') is not None and 
        request.args.get('email') is not None
        ):

        dataset_name        = request.args.get('dataset')
        this_email          = request.args.get('email')
        duration            = request.args.get('duration')
        satori_expiration   = datetime.datetime.utcnow() + datetime.timedelta(hours=int(duration)) 

        # FIRST, authenticate to Satori for a bearer token
        satori_token = satori_auth.satori_auth()

        # SECOND, find our dataset
        dataset_id = satori_dataset.get_dataset_id_by_name(satori_token, dataset_name)

        # THIRD, get overall data policy ID for the dataset
        data_policy_id = satori_dataset_policy.get_dataset_policy_id(satori_token, dataset_id)

        # FOURTH, Now add our user to this data policy
        result = satori_data_access_permission.add_user(satori_token, data_policy_id, this_email, satori_expiration)

        return render_template('adduser_result.html', result = result)

    else:
        return "error: missing or invalid info, required info is: 1) api key, 2) name of Satori Dataset, 3) duration, 4) email"