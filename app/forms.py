"""
Definition of forms.
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import StrictButton
from app.models import UserProfile
from xml.etree import ElementTree
import requests
import config

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.CharField(max_length=140)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'url',
            'address',
            'city',
            'state',
            'zip_code',
        )
        self.helper.add_input(Submit('submit', 'Save Changes'))

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')   
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()

    def parse_ugly_xml(self, text):
        doc = ElementTree.fromstring(text)
        a = doc.find('{http://www.w3.org/2005/Atom}entry')
        b = a.find('{http://www.w3.org/2005/Atom}content')
        c = b.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
        new_address = c.findtext('{http://schemas.microsoft.com/ado/2007/08/dataservices}AddressLine')
        new_suite = c.findtext('{http://schemas.microsoft.com/ado/2007/08/dataservices}Suite')
        new_address_combined = "{} {}".format(new_address, new_suite).strip()
        new_city = c.findtext('{http://schemas.microsoft.com/ado/2007/08/dataservices}City')
        new_state = c.findtext('{http://schemas.microsoft.com/ado/2007/08/dataservices}State')
        new_zip_code = c.findtext('{http://schemas.microsoft.com/ado/2007/08/dataservices}ZipCode')
        return new_address_combined, new_city, new_state, new_zip_code

    def clean(self):        
        cleaned_data = super(UserProfileForm, self).clean()
    
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
        account_key = config.azure_datamarket_access_key
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
            raise forms.ValidationError(
                "Your address was validated and updated with corrected content.  Please submit again if it is correct.")

        return cleaned_data

    class Meta:
        model = UserProfile
        exclude = ('user',)