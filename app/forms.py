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
        import requests
        from xml.etree import ElementTree
        
        cleaned_data = super(UserProfileForm, self).clean()
        
        # Validate the Address of the User
        # Get address data from cleaned data

        # Verify the address using the data marketplace service
        # https://datamarket.azure.com/dataset/melissadata/addresscheck

        # Parse the returned text

        # Compare entered address with validated address

        return cleaned_data

    class Meta:
        model = UserProfile
        exclude = ('user',)