"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

from django.core.exceptions import ValidationError
def validate_true(value):
    if value is not True:
        raise ValidationError("This value is required to be true...")

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    accepted_eula = models.BooleanField(default = False, validators=[validate_true])
    favorite_animal = models.CharField(max_length=20, default="Dragons.")
    url = models.URLField("Website", blank=True)


# create the user profile on post save of user accounts
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
