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

from route_user import satori_user

app = Flask(__name__)
app.register_blueprint(satori_user)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))