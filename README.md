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
	
## Setup the database ##
We need to setup the SQLite database. Run the syncdb command and setup a superuser (if desired) to your database.
	
	python manage.py syncdb

Next, we can populate the database with items.  I have included a management command that does this.  Images are hosted on an azure storage account.

	python manage.py populate_grocery_database

## Commit the SQLite db ##
We need to commit the db to Git so we will have it later for the Git Deployment

	git add db.sqlite3
	git commit -m 'added sqlite db'

## Go to [portal.azure.com](portal.azure.com) and make a web app (website) ##
Once you create this site feel free to leave this tab open as we will be coming back to this.

## Go back to the Azure Portal setup Continuous Deployment ##
Browse to the web app we created and click on continuous deployment.  Set this up to use local git.

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

	
# --- CODE SNIPPETS BELOW ---

# Form.py : Address Validation
        address = cleaned_data.get('address', '')
        city = cleaned_data.get('city', '')
        state = cleaned_data.get('state', '')
        zip_code = cleaned_data.get('zip_code', '')
        full_address = "'{}, {}, {} {}'".format(address, city, state, zip_code)

        # Verify the address using the data marketplace
        # https://datamarket.azure.com/dataset/melissadata/addresscheck
        uri = "https://api.datamarket.azure.com/MelissaData/AddressCheck/v1/SuggestAddresses"
        data = {'Address':full_address, 'MaximumSuggestions':1, 'MinimumConfidence':0.25}
        account_key = 'PAAWRFiAqLKRLswTxyVxT9wbb4torRFs/HpZowgPrDg='
        req = requests.get(uri, params=data, auth=('', account_key))

        if not req.ok:
            raise Exception(req.text)

        new_address_combined, new_city, new_state, new_zip_code = self.parse_ugly_xml(req.text)

        if new_address_combined != address or new_city != city or new_state != state or new_zip_code != zip_code:
            # Correct the address
            cleaned_data['address'] = new_address_combined
            cleaned_data['city'] = new_city
            cleaned_data['state'] = new_state
            cleaned_data['zip_code'] = new_zip_code
            raise forms.ValidationError("Your address was validated and updated with corrected content.  Please submit again if it is correct.")


# Views.py : Purchase Recommendations
        # use frequently bought together to get recommendations
        # https://datamarket.azure.com/dataset/amla/mba
        uri = 'https://api.datamarket.azure.com/data.ashx/amla/mba/v1/Score'
        data = {'Id':'Train', 'Item':id}
        account_key = '5dxIeDWCg/dwSclY/mvt929z26mf/RnHKNXeqDN2he8='
        req = requests.get(uri, params=data, auth=('', account_key))

        #req.text is a dictionary in text.  Can Eval it here...
        recommend = eval(req.text)['ItemSet'][1:]
        recommend_products = []

        # now that we have the id(s) of recomendations we should expand to the product
        for i in recommend:
            recommend_products.append(Product.objects.get(id=int(i)))

		# ADD TO THE RETURN
        'recommended_products':recommend_products,

#templates/app/Product.html : Purchase Recommendations
	<div class="row">
	    <h3>Here are some other things you may be interested in:</h3>
	    {% for i in recommended_products %}
	        <a href="{% url 'product' %}{{i.id}}"><img src="{{i.image_link}}" width="100"/> {{ i.name }} - ${{price}}</a> <br />
	    {% endfor %}
	</div>
