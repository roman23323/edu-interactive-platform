from django.contrib import admin

from .models import CardCollection, Card

admin.site.register([CardCollection, Card])