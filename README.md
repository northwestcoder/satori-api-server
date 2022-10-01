# satori-api-server
**A relay server for communicating with the Satori Rest API**

This is a Python Flask-based web app which communicates with the Satori platform.

It is meant to be deployed as a standalone server in such a manner that you would then connect to URL endpoints, submitting requests via parameters. This server would then call into the Satori Rest API with the info provided.

This project was tested using Google Cloud Run; The dockerfile included here is ready to go for GCP. Short steps to deploy this project are:

- Install ```gcloud``` command line tools (we have tested on macOS)
- Log into google cloud from the command line with ```gcloud auth login```
- Set your project with ```gcloud config set project YOUR_PROJECT_ID```
- Make sure Google Cloud Run API's are enabled for this project
- Create a new file ```satori.py``` with this content:

```
apikey 			= ""
serviceaccount_id 	= ""
serviceaccount_key	= ""
account_id		= ""
apihost			= "app.satoricyber.com"
security_policy_id	= ""
```

- Fill in all of the values in this new ```satori.py``` file or else this example will fail. 
	- Use the Satori documentation to find account and service account info. 
	- apihost defaults to app.satoricyber.com
	- security_policy_id has to be looked up manually in the UX
	- apikey is a made up token/secret to protect this relay server. Enter a unique and strong value and then use that value in url requests (see below)
- Deploy this project: navigate to where you have downloaded it, and run: ```gcloud run deploy```

You can run locally with:

- ```pip install -r requirements.txt```
- ```python main.py```

___

We have one simple example, https://<the.gcloud.deployed.url.app>/adduser. This endpoint will add a user to a Satori Dataset with a specified security policy and a specified duration.


The ```/adduser``` path expects the following parameters:

- apikey: a key we made up and put in ```satori.py```. If your incoming parameter value doesn't match, we will fail.
- email: the email/login for the user you want to add.
- dataset: the name of the Satori Dataset to which you want to add this email/user.
- duration: the number of hours this permission is allowed, after which the permission will expire.

Complete URL Example: 

```https://<the.gcloud.deployed.url.app>/adduser?apikey=asdklj33489&email=youremail@yourcompany.com&dataset=A%20Satori%20Dataset&duration=20```

This would add youremail@yourcompany.com to a Satori dataset called "A Satori Dataset" for the next 20 hours.

