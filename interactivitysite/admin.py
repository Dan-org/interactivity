from django.contrib import admin
from models import Page


### Unregsiter Clutter ###

from django.contrib.auth.models import Group
admin.site.unregister(Group)