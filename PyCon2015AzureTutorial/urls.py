"""
Definition of urls for PyCon2015AzureTutorial.
"""

from datetime import datetime
from django.conf.urls import patterns, url

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^product/', 'app.views.product', name='product'),
    url(r'^profile', 'app.views.profile', name='profile'),
    url(r'^accounts/', include('registration.backends.simple.urls'), name = 'accounts'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
