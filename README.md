# Welcome to the PyCon 2015 Azure Tutorial #

## Overview ##
1. Get an Azure Account
2. Clone the git repo
3. Setup Environment
4. Create an Azure Web App/Website
5. Deploy to Azure using Git Deployment
6. Add Address Validation using Azure Data Marketplace offering
7. Add Purchase Recommendation using Azure Data Marketplace offering.
8. App Insights

## Get an Azure account ##
Go to [http://aka.ms/AzureTrial](http://aka.ms/AzureTrial) and get a trial.

## Clone this Repo ##
	git clone https://github.com/crwilcox/PyCon2015AzureTutorial.git

## Create Virtual Environment and install requirements ##
	python -m venv env
	pip install -r requirements.txt

## Go to [portal.azure.com](portal.azure.com) and make a web app (website) ##
Once you create this site feel free to leave this tab open as we will be coming back to this.

## Go back to the Azure Portal setup Continuous Deployment ##
Browse to the web app we created and click on continuous deployment.  Set this up to use local git.
If this is your first time setting up a site you will need to create a deployment user as well.

NOTE: if for some reason you see 'null' as your username go to Deployment Credentials and try again.

After this, go to settings for the web app you created will be a string for git that resembles this:
 
	https://USER@WEB_APP_NAME.scm.azurewebsites.net:443/WEB_APP_NAME.git

## Setup the database ##
We need to setup the SQLite database. Run the syncdb command and setup a superuser (if desired) to your database.
	
	python manage.py syncdb

Next, we can populate the database with items.  I have included a management command that does this.  Images are hosted on an azure storage account.

	python manage.py populate_grocery_database

## Commit the SQLite db ##
We need to commit the db to Git so we will have it later for the Git Deployment

	git add db.sqlite3
	git commit -m 'added sqlite db'

## Push your changes to the git deployment ##

	git remote add azure https://USER@WEB_APP_NAME.scm.azurewebsites.net:443/WEB_APP_NAME.git
	git push azure master

The first push takes a bit as it will setup the environment and django installs quite a few things.  No worries though, we will continue along while it does its thing.

# Adding Functionality to the site #
# Monitoring and Logging
## App Insights ##
Getting AppInsights running in your django app is very straightforward.

Go to the Azure portal and browse under Application Insights.  There should be an instance under the same name as your Django Website.

Get the instrumentation key under settings to insert to the below code

pip install applicationinsights

To get unhandled exception handling: open app/\_\_init\_\_.py and add the following to the beginning

	from applicationinsights.exceptions import enable
	enable('<YOUR INSTRUMENTATION KEY GOES HERE>')

Logging PageViews.  In views.py
	
	from applicationinsights import TelemetryClient
	tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
	
	# in each view you want to track
    tc.track_pageview('home', request.get_full_path(), properties = {'username': request.user.username})
    tc.flush()

Go to [https://github.com/Microsoft/AppInsights-Python](https://github.com/Microsoft/AppInsights-Python) for more examples

## The Azure Marketplace ##
Provides many data offerings that are free or available for a small fee.  Most offerings have a certain amount for no cost.  Everything we use today is currently offered in some form for free.

This market place includes things authored by Microsoft as well as third parties.  You can offer these as well if you would like for users.

[Browse The Microsoft Azure Marketplace](https://datamarket.azure.com/browse)
If this is your first time to the Marketplace you may have to register for azure market place account. This is a simple process though and only involves your name and email

## Add Support for Address Validation ##
This offering is offered by Melissa Data.  This is an example of a third party selling their data service on the Azure Data Market

1. Use Azure Marketplace: [https://datamarket.azure.com/dataset/melissadata/addresscheck](https://datamarket.azure.com/dataset/melissadata/addresscheck)

## Add Support for Product Recommendations ##
This offering is made by Azure ML and is an example of an offering from Microsoft.

Use Azure Marketplace: [https://datamarket.azure.com/dataset/amla/mba](https://datamarket.azure.com/dataset/amla/mba)

We can train our model here: [https://marketbasket.cloudapp.net/](https://marketbasket.cloudapp.net/)

## Azure ML ##
I mentioned the above sample is from Azure ML.  We offer a data studio experience for authoring these offerings.  It allows you to make your own predictive models and publish them for consumption for yourself or others.

[https://studio.azureml.net/](https://studio.azureml.net/ "https://studio.azureml.net/")
