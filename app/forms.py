"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import UserProfile

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.CharField(max_length=140)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

        # Order Elements to make the page look better
        self.fields.keyOrder = ['first_name',
            'last_name',
            'email',
            'url',
            'address',
            'city',
            'state',
            'zip_code',]

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')   
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()

    def clean(self):
        import requests
        from xml.etree import ElementTree
        
        cleaned_data = super(UserProfileForm, self).clean()
        
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
        text = req.text
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

        if new_address_combined != address or new_city != city or new_state != state or new_zip_code != zip_code:
            # Correct the address
            cleaned_data['address'] = new_address_combined
            cleaned_data['city'] = new_city
            cleaned_data['state'] = new_state
            cleaned_data['zip_code'] = new_zip_code
            raise forms.ValidationError("Your address was validated and updated with corrected content.  Please submit again if it is correct.")

        return cleaned_data

    class Meta:
        model = UserProfile
        exclude = ('user',)