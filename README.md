# Welcome to the Azure Fresh Sample

You can skip steps if you would like.  The sample covers the following.
## Overview ##
1. [Get an Azure Account](#1)
2. [Cloning this repo](#2)
3. [Setup Virtual Environment for the Django App](#3)
4. [Create an Azure Web App/Website to host this site](#4)
5. [Deploy to Azure using Git Deployment](#5)
6. [Adding Application Insights Support to our App](#6)
7. [Add Address Validation using Azure Data Marketplace offering from MelissaData](#7)
8. [Add Purchase Recommendation using Azure Data Marketplace offering from the Azure ML team.](#8)

Note: Many of the steps in this tutorial are completed in the live code.  This isn't so much a tutorial as an example of how you might use these services.  Instructions are provided to help it be more obvious how you could use this code in your scenario.

<div id='1'/>
## Get an Azure account ##
Go to [http://aka.ms/AzureTrial](http://aka.ms/AzureTrial) and get a trial.

<div id='2'/>
## Clone this Repo ##
	git clone https://github.com/crwilcox/AzureFresh.git

<div id='3'/>
## Create Virtual Environment and install requirements ##
	python -m venv env
	pip install -r requirements.txt

<div id='4'/>
## Go to [portal.azure.com](portal.azure.com) and make a web app (website) ##
Once you create this site feel free to leave this tab open as we will be coming back to this.

<div id='5'/>
## In the Azure Portal setup Continuous Deployment ##
Browse to the web app we created and click on continuous deployment.  Set this up to use local git.
If this is your first time setting up a site you will need to create a deployment user as well.

NOTE: if for some reason you see 'null' as your username go to Deployment Credentials and try again.

After this, go to settings for the web app you created will be a string for git that resembles this:
 
	https://USER@WEB_APP_NAME.scm.azurewebsites.net:443/WEB_APP_NAME.git

## Push your changes to the git deployment ##

	git remote add azure https://USER@WEB_APP_NAME.scm.azurewebsites.net:443/WEB_APP_NAME.git
	git push azure master

The first push takes a bit as it will setup the environment and django installs quite a few things.  No worries though, we will continue along while it does its thing.

# Adding Functionality to the site #
# Monitoring and Logging

<div id='6'/>
## App Insights ##
Getting AppInsights running in your django app is very straightforward.

Go to the Azure portal and browse under Application Insights.  There should be an instance under the same name as your Django Website.

Get the instrumentation key under settings to use as the parameter for creating clients.

pip install applicationinsights

Add applicationinsights to requirements.txt so when we deploy to azure this is present.

### Add JavaScript Snippet to get logging for site ###
When under the application insights page click on one of the not-yet-done graphs.  This should get you to a tab that has the ability to get a snippet.  Copy this snippet into layout.html and you will get client side logging of things like response and page views

### Using WSGI Middleware to get a good amount of logging for free ###

In wsgi.py we can add a few lines at the end of the file which will give us a large amount of the logging for free.

	from applicationinsights.requests import WSGIApplication
	application = WSGIApplication('<YOUR INSTRUMENTATION KEY GOES HERE>', application)

### Unhandled Exception Logging ###
Application Insights supports handling unhandled exceptions.  To get this handling: open app/\_\_init\_\_.py and add the following to the beginning

	from applicationinsights.exceptions import enable
	enable('<YOUR INSTRUMENTATION KEY GOES HERE>')

### Logging events manually ###
Application Insights also supports manual event logging.  You can log, for instance, we can send an event when the homepage is loaded by adding the following code.
	
	from applicationinsights import TelemetryClient
	tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
	
	# in each view you want to track
    tc.track_event('home page loaded')

Go to [https://github.com/Microsoft/AppInsights-Python](https://github.com/Microsoft/AppInsights-Python) for more examples

## The Azure Marketplace ##
Provides many data offerings that are free or available for a small fee.  Most offerings have a certain amount for no cost.  Everything we use today is currently offered in some form for free.

This market place includes things authored by Microsoft as well as third parties.  You can offer these as well if you would like for users.

[Browse The Microsoft Azure Marketplace](https://datamarket.azure.com/browse)
If this is your first time to the Marketplace you may have to register for azure market place account. This is a simple process though and only involves your name and email

<div id='7'/>
## Add Support for Address Validation ##
This offering is offered by Melissa Data.  This is an example of a third party selling their data service on the Azure Data Market

[https://datamarket.azure.com/dataset/melissadata/addresscheck](https://datamarket.azure.com/dataset/melissadata/addresscheck)

In forms.py under the clean method, we want to add the following code to validate our address using the data returned by the user form.

```python
		# Validate the Address of the User
        # Get address data from cleaned data
        address = cleaned_data.get('address', '')
        city = cleaned_data.get('city', '')
        state = cleaned_data.get('state', '')
        zip_code = cleaned_data.get('zip_code', '')

        # Verify the address using the data marketplace service
        # https://datamarket.azure.com/dataset/melissadata/addresscheck
        full_address = "'{}, {}, {} {}'".format(address, city, state, zip_code)
        uri = "https://api.datamarket.azure.com/MelissaData/AddressCheck/v1/SuggestAddresses"
        data = {'Address':full_address, 'MaximumSuggestions':1, 'MinimumConfidence':0.25}
        account_key = 'YOUR_DATA_KEY_GOES_HERE'
        req = requests.get(uri, params=data, auth=('', account_key))

        # Parse the returned text
        new_address_combined, new_city, new_state, new_zip_code = self.parse_ugly_xml(req.text)

        # Compare entered address with validated address
        if new_address_combined != address or new_city != city or new_state != state or new_zip_code != zip_code:
            # Correct the address
            cleaned_data['address'] = new_address_combined
            cleaned_data['city'] = new_city
            cleaned_data['state'] = new_state
            cleaned_data['zip_code'] = new_zip_code
            raise forms.ValidationError("Your address was validated and updated with corrected content.  Please submit again if it is correct.")
```

<div id='8'/>
## Add Support for Product Recommendations ##
This offering is made by Azure ML and is an example of an offering from Microsoft.

[https://datamarket.azure.com/dataset/amla/recommendations](https://datamarket.azure.com/dataset/amla/recommendations)

For this example we are going to use a python library from [https://github.com/crwilcox/RecommendationService](https://github.com/crwilcox/RecommendationService).  This library wraps the web calls in a way that is more easy for us to use.

There are two parts to using the recommendations service.  We need to build a model and consume a model. We only need to build a model once but we expect to consume our model frequently.

### Building our Model

```python
email = 'email@outlook.com'
key = '1faKeFAKe/ijKeyS/for234r56st/DeMoYZcoDE7EF8='
rs = RecommendationService(email, key)

# create model
model_id = rs.create_model('groceries' + datetime.now().strftime('%Y%m%d%H%M%S'))

# import item catalog
catalog_path = os.path.join('app', 'management', 'commands', 'catalog.csv')
rs.import_file(model_id, catalog_path, Uris.import_catalog)

# import usage information
transactions_path = os.path.join('app', 'management', 'commands', 'transactions.csv')
rs.import_file(model_id, transactions_path, Uris.import_usage)

# build model
build_id = rs.build_fbt_model(model_id)
status = rs.wait_for_build(model_id, build_id)

if status != BuildStatus.success:
    print('Unsuccessful in building the model, failing now.')
    return

# update model active build (not needed unless you are rebuilding)
rs.update_model(model_id, None, build_id)

print('Built a model. Model ID:{} Build ID:{}'.format(model_id, build_id))
```

### Consuming our Model (Getting Recommendations)

This is done in model.py under the Product class.  Here is a sample of how you can consume this service.

```python
 	# Use data marketplace service to get recommendations
	email = 'email@outlook.com'
	key = '1faKeFAKe/ijKeyS/for234r56st/DeMoYZcoDE7EF8='
    rs = RecommendationService(email, key)
    recommendations = rs.get_recommendation(config.model_id, [ str(id) ])
    recommend_products = [ Product.objects.get(id=int(r.id)) for r in recommendations ]
```