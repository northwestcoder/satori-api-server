import json
import requests
import time

from satori import satori
from satori import satori_common
from satori import satori_location


def add_tag_to_satori(headers, satori_datastore_id, search, column_name, tag_to_change):
	
	locations = satori_location.get_one_location_by_datastore_and_search(headers, satori_datastore_id, search + "." + column_name)

	for location in locations.json()["records"]:

		location_id = location["id"]
		table = location["location"]["table"]
		if "tags" in location and location["tags"] != None:
			for existing_tag in location["tags"]:
				if existing_tag["name"] == tag_to_change.upper():
					print("Tag {} already exists".format(existing_tag["name"]))
					return
		print("Adding tag to {}".format(location_id))

		url = "https://{}/api/locations/{}".format(satori.apihost, location_id)
		r = requests.put(url, headers=headers, data='{"addTags": ["' + tag_to_change + '"], "removeTags": [], "notes": "Inherited from Collibra"}')
