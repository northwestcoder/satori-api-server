import os
import json
import requests
import time
import datetime
import io
from flask import Flask, redirect, url_for, render_template, request, session

import satori
import auth
import dataset
import dataset_policy
import data_access_permission

app = Flask(__name__)

@app.route('/adduser', methods=['GET'])
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
        satori_token = auth.satori_auth()

        # SECOND, find our dataset
        dataset_id = dataset.get_dataset_id_by_name(satori_token, dataset_name)

        # THIRD, get overall data policy ID for the dataset
        data_policy_id = dataset_policy.get_dataset_policy_id(satori_token, dataset_id)

        # FOURTH, Now add our user to this data policy
        result = data_access_permission.add_user(satori_token, data_policy_id, this_email, satori_expiration)

        return render_template('adduser_result.html', result = result)

    else:
        return "error: missing or invalid info, required info is: 1) api key, 2) name of Satori Dataset, 3) duration, 4) email"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))