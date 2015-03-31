# Welcome to the PyCon 2015 Azure Tutorial #

## Overview ##
1. Deploy to Azure using Git Deployment
2. Add Address Validation using Azure Data Marketplace offering
3. Add Purchase Recommendation using Azure Data Marketplace offering.
4. App Insights

## Clone this Repo ##
	git clone https://github.com/crwilcox/PyCon2015AzureTutorial.git

## Setup the database ##
We need to setup the SQLite database. Run the syncdb command and setup a superuser (if desired) to your database.
	
	python manage.py syncdb

Next, we can populate the database with items.  I have included a management command that does this.

	python manage.py populate_grocery_database

## Go to portal.azure.com and make a web app (website) ##
We need to go create a web site to publish to.  
Leave this tab open as we are coming back here.

## Commit the SQLite db ##
We need to commit the db to Git so we will have it later for the Git Deployment

	git add db.sqlite3
	git commit -m 'added sqlite db'

## Go back to the Azure Portal setup Continuous Deployment ##
Browse to the web app we created and click on continuous deployment.  Set this up to use local git.

After this, go to settings for the web app you created will be a string for git that resembles this:
 
	https://USER@WEB_APP_NAME.scm.azurewebsites.net:443/WEB_APP_NAME.git

## Push your changes to the git deployment ##

	Git remote add azure https://USER@WEB_APP_NAME.scm.azurewebsites.net:443/WEB_APP_NAME.git
	Git push azure master

The first push takes a bit as it will setup the environment and django installs quite a few things

# To Add #
## The Azure Marketplace ##
Provides many data offerings that are free or available for a small fee.  Most offerings have a certain amount for no cost.  Everything we use today is currently offered in some form for free.

This market place includes things authored by Microsoft as well as third parties.  You can offer these as well if you would like for users.

[Browse The Microsoft Azure Marketplace](https://datamarket.azure.com/browse)

## Add Support for Product Recommendations ##
This offering is made by Azure ML and is an example of an offering from Microsoft.

Use Azure Marketplace: [https://datamarket.azure.com/dataset/amla/mba](https://datamarket.azure.com/dataset/amla/mba)

We can train our model here: [https://marketbasket.cloudapp.net/](https://marketbasket.cloudapp.net/)

Include code Snippets

## Azure ML ##
I mentioned the above sample is from Azure ML.  We offer a data studio experience for authoring these offerings.  It allows you to make your own predictive models and publish them for consumption for yourself or others.

[https://studio.azureml.net/](https://studio.azureml.net/ "https://studio.azureml.net/")

## Add Support for Address Validation ##
This offering is offered by Melissa Data.  This is an example of a third party selling their data service on the Azure Data Market

1. Use Azure Marketplace: [https://datamarket.azure.com/dataset/melissadata/addresscheck](https://datamarket.azure.com/dataset/melissadata/addresscheck)

2. TODO: include code snippets here

## App Insights ##
Getting AppInsights running in your django app is very straightforward.

1. Go to the Azure portal and browse under Application Insights.  There should be an instance under the same name as your Django Website.

2. Get the id of that instance under settings

3. pip install applicationinsights

4. Open app/\_\_init\_\_.py and add the following to the beginning

	from applicationinsights.exceptions import enable
	# set up exception capture

	enable('<YOUR INSTRUMENTATION KEY GOES HERE>')

5. Go to https://github.com/Microsoft/AppInsights-Python for more examples

	
