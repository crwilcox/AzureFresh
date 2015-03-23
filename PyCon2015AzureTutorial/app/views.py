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

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

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
                form_errors.append((form.fields[i].label, form.errors[i]))

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

