# satori-api-server
**A relay server for communicating with the Satori Rest API**

This is a Python Flask-based web app which communicates with the Satori platform. It is meant to be deployed as a standalone server, receiving URLs and parameters via a single GET (occassionally some POSTS) and then submitting requests to the Satori API using those parameters. 

This is an example project meant for tutorial and learning purposes only.

##### Table of Contents  
[Deploy](#deploy)  
[Add/Remove Satori Users](#users)  
[Add/Remove Satori Groups](#groups)  
[Query Other Satori Info](#other)  
[Get One Satori Taxonomy](#one_taxonomy)  
[Create Satori Taxonomy](#create_taxonomy)  
[Query Satori Locations](#locations)  

___

<a name="deploy"/>

## Deployment

**GCP**: This project was tested using Google Cloud Run. The dockerfile included here is ready to go for GCP. Short GCP-specific steps to deploy this project:

1. Install ```gcloud``` command line tools (we have tested on macOS)
2. Log into google cloud from the command line with ```gcloud auth login```
3. Set your project with ```gcloud config set project YOUR_PROJECT_ID```
4. Make sure Google Cloud Run API's are enabled for this project
5. Create a new file ```satori.py``` with this content:

```
account_id		= "YOUR_SATORI_ACCOUNT_ID"
serviceaccount_id 	= "YOUR_SATORI_SERVICE_ACCOUNT_ID"
serviceaccount_key	= "YOUR_SATORI_SERVICE_ACCOUNT_KEY"
apihost			= "app.satoricyber.com"
apikey 			= "YOUR_NEW_MADE_UP_KEY"
logging 		= True
```

6. Update all of the values (using the quotes) in your new ```satori.py``` file or else this example will fail. 
	- Use the Satori [documentation](https://app.satoricyber.com/docs/api) to find ```account_id```, ```serviceaccount_id``` and ```serviceaccount_key``` info. 
	- ```apihost```: defaults to app.satoricyber.com, this can be left as is unless instructed otherwise.
	- ```apikey```: this is a made up token/secret for this python example, to protect this relay server. 
		- Enter a unique and strong value here, and then also use that value in url requests or in the http header (either is supported)
		- Note: this is a test harness - in production, instead of storing a secret or key inside code, you should instead look it up from a secret manager!
	- ```logging```: If ```True```, detailed info is output to the console for debugging.

7. Deploy this project: navigate to where you have downloaded it, and run: ```gcloud run deploy```

**AWS**: with some changes and testing, this docker/code approach will probably also work with AWS, e.g. their "app runner" product. 

**Local deployment**: 

1. We tested with python 3.10.4 and recommend [pyenv](https://github.com/pyenv/pyenv) for your environment management. Assuming your python env is up and running:
2. Create the satori.py file as above.
3. at the command line:
- ```pip install -r requirements.txt```
- ```python main.py```


___

EXAMPLES:

Once you have this flask server running in GCP or some cloud manner, you would connect to it via HTTPS for GETS and you would use a tool like Postman for POSTS.

<a name="users"/>


## Generic _/satori/user/add_ and _/satori/user/remove_ routes

Method: GET 

These endpoints will add or remove a user (specifically, their email address) to a Satori Dataset with a specified security policy and a specified duration.

These paths expects the following parameters:

- apikey: a key we made up and put in ```satori.py```. If your incoming parameter value doesn't match, we will fail.
- email: the email/login for the user you want to add.
- dataset: the name of the Satori Dataset to which you want to add this email/user.
- duration: the number of hours this permission is allowed, after which the permission will expire.
- Satori security policy id: you need to look these ID's up in the UX currently.

A Complete URL Example: 

```
http://<the.gcloud.deployed.url.app>/satori/user/add?apikey=YOURAPIKEY&dataset=Secured%20Data&email=john123.789smith@gmail.com&duration=20&security_policy_id=SATORI_SECURITY_POLICY_ID
```

- This would add john123.789smith@gmail.com to a Satori dataset called "Secured Data" with 20 hours of access and would assign john a specific security policy for those 20 hours.
- If the URL request is successful, depending on your client, you will see a web page with the datastores being managed by the Dataset you are trying to connect to.
- The underlying API for this example is available [here](https://app.satoricyber.com/docs/api#post-/api/v1/data-access-rule/instant-access). The example POST body/payload is found in satori_data_access_users.py


To remove a user, just change "add" to "remove" in the URL path. You will no longer need the ```security_policy_id``` or ```duration``` parameters:

```
http://<the.gcloud.deployed.url.app>/satori/user/remove?apikey=YOURAPIKEY&dataset=Secured%20Data&email=john123.789smith@gmail.com
```

<a name="groups"/>


## Generic _/satori/group/add_ and _/satori/group/remove_ routes

Method: GET

Similar to ```user``` above, these paths will add a Satori Local Group by name. If more than one group matches your URL, this code will add the first entry found.

e.g. 

```
http://<the.gcloud.deployed.url.app>/satori/group/add?apikey=YOURAPIKEY&dataset=Secured%20Data&groupname=Data%20Science%20Team&duration=20&security_policy_id=SATORI_SECURITY_POLICY_ID
http://<the.gcloud.deployed.url.app>/satori/group/remove?apikey=YOURAPIKEY&dataset=Secured%20Data&groupname=Data%20Science%20Team&duration=20&security_policy_id=SATORI_SECURITY_POLICY_ID
```

<a name="other"/>

## Generic /satori/other/TYPE

Method: GET

e.g. 

```
http://<the.gcloud.deployed.url.app>/satori/other/custom_taxonomy
http://<the.gcloud.deployed.url.app>/satori/other/datasets
http://<the.gcloud.deployed.url.app>/satori/other/data_access_controllers
http://<the.gcloud.deployed.url.app>/satori/other/datastores
http://<the.gcloud.deployed.url.app>/satori/other/masking
http://<the.gcloud.deployed.url.app>/satori/other/security_policies
http://<the.gcloud.deployed.url.app>/satori/other/taxonomy
```

For debugging or utility purposes, these routes returns various other types of information in Satori


<a name="one_taxonomy"/>

## Find one Custom Taxonomy

Method: GET

- For integrations with external data catalogue or inventory systems, this is a useful lookup pattern.
- You can search by "name", "id" or "tag"
- The general form of these GETS are:
	- ```http://<the.gcloud.deployed.url.app>/satori/taxonomy/find_by_id?search=YOURID```
	- ```http://<the.gcloud.deployed.url.app>/satori/taxonomy/find_by_name?search=YOURNAME```
	- ```http://<the.gcloud.deployed.url.app>/satori/taxonomy/find_by_tag?search=YOURTAG```
	- where \<action\> is "name", "id" or "tag"
- This will return a payload with the rest of the Custom Taxonomy, e.g. something like:

```
{
  "config": {
    "additionalSatoriCategoriesToTag": [],
    "fieldNamePattern": null,
    "fieldType": null,
    "satoriBaseClassifierId": null,
    "type": "NON_AUTOMATIC",
    "values": {
      "caseInsensitive": false,
      "regex": false,
      "values": []
    }
  },
  "createdAt": 1658520471138,
  "description": "",
  "id": "AN_ID_HERE",
  "name": "custom_classifier",
  "nameCreatedBy": "John Smith",
  "nameUpdatedBy": "Jane Doe",
  "nodeType": "CLASSIFIER",
  "parentNode": "AN_ID_HERE",
  "scope": {
    "datasetIds": [],
    "includeLocations": []
  },
  "tag": "c12n_custom.Acme Specific Data or Column::custom_classifier",
  "updatedAt": 1658520471138
}
```

<a name="create_taxonomy"/>

## Create A Single Custom Taxonomy

Method: POST

Experimental

/satori/taxonomy/create

Expects a valid json body for the post, see [Satori Docs](https://app.satoricyber.com/docs/api#post-/api/v1/taxonomy/custom/classifier) for more info.


<a name="locations"/>

## Find Database Locations and Classifiers for a Datastore

Method: GET

There are two paths and methods in this example:

First, you can retrieve all schema/table/column info associated with a Satori Datastore by using:

```/satori/location/get_locations_by_datastore?datastore_id=YOUR_DATASTORE```

This is the raw full list of all schemas, tables and columns that Satori has discovered.

Second, you can retrieve all of the above, but only for info which has been classified by Satori (or by you, by hand):

```/satori/location/get_tags_by_datastore?datastore_id=YOUR_DATASTORE```
