from django.contrib import admin

from accounts.models import Profile, Account

admin.site.register(Profile)
admin.site.register(Account)