import os
import json
import requests
import time
import datetime
import io

from flask import Flask, redirect, url_for, render_template, request, session

from satori import satori
from satori import satori_common
from satori import satori_dataset
from satori import satori_dataset_policy
from satori import satori_data_access_users
from satori import satori_data_access_groups

from routes.route_user import satori_user
from routes.route_group import satori_group
from routes.route_others import satori_others
from routes.route_taxonomy import satori_taxonomy
from routes.route_location import satori_location
from routes.route_scandb import satori_route_scandb
from routes.route_collibra import satori_collibra




app = Flask(__name__)
app.register_blueprint(satori_user)
app.register_blueprint(satori_group)
app.register_blueprint(satori_others)
app.register_blueprint(satori_taxonomy)
app.register_blueprint(satori_location)
app.register_blueprint(satori_route_scandb)
app.register_blueprint(satori_collibra)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    satori_token = satori_common.satori_auth()