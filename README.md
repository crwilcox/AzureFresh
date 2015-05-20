# Welcome to the PyCon 2015 Azure Tutorial #

## Overview ##
1. Get an Azure Account
2. Clone the git repo
3. Setup Environment
4. Create an Azure Web App/Website
5. Deploy to Azure using Git Deployment
6. App Insights
7. Add Address Validation using Azure Data Marketplace offering
8. Add Purchase Recommendation using Azure Data Marketplace offering.


## Get an Azure account ##
Go to [http://aka.ms/AzureTrial](http://aka.ms/AzureTrial) and get a trial.

## Clone this Repo ##
	git clone https://github.com/crwilcox/PyCon2015AzureTutorial.git

## Create Virtual Environment and install requirements ##
	python -m venv env
	pip install -r requirements.txt

## Go to [portal.azure.com](portal.azure.com) and make a web app (website) ##
Once you create this site feel free to leave this tab open as we will be coming back to this.

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

## Add Support for Address Validation ##
This offering is offered by Melissa Data.  This is an example of a third party selling their data service on the Azure Data Market

[https://datamarket.azure.com/dataset/melissadata/addresscheck](https://datamarket.azure.com/dataset/melissadata/addresscheck)

For code see spoilers.txt

## Add Support for Product Recommendations ##
This offering is made by Azure ML and is an example of an offering from Microsoft.

[https://datamarket.azure.com/dataset/amla/mba](https://datamarket.azure.com/dataset/amla/mba)

We can train our model here: [https://marketbasket.cloudapp.net/](https://marketbasket.cloudapp.net/)

For code see spoilers.txt 

## Azure ML ##
I mentioned the above sample is from Azure ML.  We offer a data studio experience for authoring these offerings.  It allows you to make your own predictive models and publish them for consumption for yourself or others.

[https://studio.azureml.net/](https://studio.azureml.net/ "https://studio.azureml.net/")
