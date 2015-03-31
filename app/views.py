"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from app.models import UserProfile
from app.forms import UserProfileForm
from app.models import Product

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    products = Product.objects.order_by('id')

    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'products':products,
        })
    )

def product(request):
    assert isinstance(request, HttpRequest)

    try:
        import requests

        # get id
        id = int(request.path.split('/')[-1])
        product = Product.objects.get(id=id)

        # Figure out recommended purchases.

        """Renders the product page."""
        return render(
            request,
            'app/product.html',
            context_instance = RequestContext(request,
            {
                'title':product.name,
                'description':product.description,
                'price':product.price,
                'image':product.image_link,
                'year':datetime.now().year,
            })
        )
    except:
        return home(request)
    

@login_required
def profile(request):
    form_errors = None
    try:
        user_profile = request.user.userprofile
    except ObjectDoesNotExist:
        # While not strictly necessary, if there was a user created before
        # introducing a user profile, we will need to create the object.
        user_profile = UserProfile.objects.create(user=request.user)
        user_profile.save()

    """ Process the post request for form """
    if request.method == 'POST':
        form = UserProfileForm(request.POST,instance=user_profile)
        if form.is_valid(): # All validation rules pass
            form.save()
        else:
            # Transform field name to label name and put in tuple with errors
            form_errors = []
            for i in form.errors:
                try:
                    label = form.fields[i].label if form.fields[i].label is not None else i
                    form_errors.append((label, form.errors[i]))
                except:
                    form_errors.append(('Error', form.errors[i]))

    """Renders the profile page."""
    assert isinstance(request, HttpRequest)
    user_profile_form = UserProfileForm(instance=user_profile)
    return render(
        request,
        'registration/profile.html',
        context_instance = RequestContext(request,
        {
            'title':'Profile',
            'message':'User Profile Information',
            'year':datetime.now().year,
            'user_profile': user_profile,
            'form':user_profile_form,
            'form_errors':form_errors,
        })
    )
