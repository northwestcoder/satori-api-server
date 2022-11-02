# satori-api-server
**A relay server for communicating with the Satori Rest API**

This is a Python Flask-based web app which communicates with the Satori platform. It is meant to be deployed as a standalone server, receiving URLs and parameters via a single GET, and then submitting requests to the Satori API using those parameters. 

This project was tested using Google Cloud Run. The dockerfile included here is ready to go for GCP. Short GCP-specific steps to deploy this project:

- Install ```gcloud``` command line tools (we have tested on macOS)
- Log into google cloud from the command line with ```gcloud auth login```
- Set your project with ```gcloud config set project YOUR_PROJECT_ID```
- Make sure Google Cloud Run API's are enabled for this project
- Create a new file ```satori.py``` with this content:

```
account_id		= ""
serviceaccount_id 	= ""
serviceaccount_key	= ""
apihost			= "app.satoricyber.com"
apikey 			= ""
```

- Fill in all of the values (using the quotes) in your new ```satori.py``` file or else this example will fail. 
	- Use the Satori documentation to find account and service account info. 
	- ```apihost```: defaults to app.satoricyber.com
	- ```apikey```: is a made up token/secret to protect this relay server. Enter a unique and strong value here, and then also use that value in url requests, see below. Note: this is a test harness - in production, instead of storing a secret or key inside code, you should instead look it up from a secret manager!
	- ```security_policy_id```: the desired Policy, its ID has to be known ahead of time and looked up manually in the Satori UX, and then used in the URL parameters.

- Deploy this project: navigate to where you have downloaded it, and run: ```gcloud run deploy```

For AWS, with some testing this docker/code approach will probably also work with AWS, e.g. their "app runner" product. 

Finnaly, you can also run this flask server locally, we tested with python 3.10.4 and recommend ```pyenv``` for your environment management:

- ```pip install -r requirements.txt```
- ```python main.py```

___

EXAMPLES:

Once you have this flask server running, you would connect to it via HTTPS.

**1. Generic _/satori/user/add_ and _/satori/user/remove_ routes**

These endpoints will add or remove a user to a Satori Dataset with a specified security policy and a specified duration.

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


To remove a user, just change "add" to "remove" in the URL path. You will no longer need the ```security_policy_id``` or ```duration``` parameters:

```
http://<the.gcloud.deployed.url.app>/satori/user/add?apikey=YOURAPIKEY&dataset=Secured%20Data&email=john123.789smith@gmail.com
```