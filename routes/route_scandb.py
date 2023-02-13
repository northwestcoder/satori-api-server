import requests
import json
from flask import Flask, redirect, url_for, Blueprint, request, render_template, session
import datetime
import time

from satori import satori
from satori import satori_common
from satori import satori_bearer_token
from satori import satori_errors as error
from satori import satori_scandb as scandb

satori_route_scandb = Blueprint('satoriscandb', __name__)

@satori_route_scandb.route('/satori/scandb', methods=['GET'])
def satori_route_postgres_scandb():

	if satori.apikey in (request.args.get('apikey'), request.headers.get('apikey')):
		# Authenticate to Satori for a bearer token every hour, else use cache
		headers = satori_bearer_token.check_token()
		if None not in (request.args.get('schema'), request.args.get('mode'), request.args.get('hostname'), request.args.get('dbname')):
			print("attempting to scan locations") if satori.logging else None
			response = scandb.scan_schema(request.args.get('hostname'), request.args.get('dbname'), request.args.get('schema'), satori.postgres_scan_user, satori.postgres_scan_pw, request.args.get('mode'))
			return "scan complete"
		else:
			return error.USER_PARAMS_MISSING
	else:
		return error.INVALID_APIKEY

