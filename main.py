import os
import json
import requests
import time
import datetime
import io
from flask import Flask, redirect, url_for, render_template, request, session

import satori
import satori_auth
import satori_dataset
import satori_dataset_policy
import satori_data_access_permission

from route_sfdc_adduser import sfdc_adduser
from route_jira import jira 

app = Flask(__name__)

#our salesforce example, see route_sfdc_adduser.py for details
app.register_blueprint(sfdc_adduser)
app.register_blueprint(jira)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))