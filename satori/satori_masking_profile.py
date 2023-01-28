import json
import requests

from satori import satori
from satori import satori_common


def get_all_masking_profiles(headers):

	url = "https://{}/api/v1/masking?accountId={}&pageSize=1000".format(satori.apihost, satori.account_id)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		print("retrieved masking profiles") if satori.logging else None
		return response.json()