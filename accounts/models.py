from datetime import datetime

import jwt

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import six
from django.utils.crypto import salted_hmac, constant_time_compare
from django.utils.http import int_to_base36, base36_to_int

from experimentorio.settings import SECRET_KEY


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    public = models.BooleanField(default=True)
    bio = models.TextField(max_length=500, blank=True, default='', verbose_name='Biography')
    github_account = models.CharField(max_length=250, blank=True, default='')
    twitter_username = models.CharField(max_length=250, blank=True, default='')
    website = models.CharField(max_length=250, blank=True, default='')
    workplace = models.CharField(max_length=250, blank=True, default='')
    verified_email = models.BooleanField(default=False)
    time_zone = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def first_name(self):
        return self.user.first_name

    @first_name.setter
    def first_name(self, name):
        self.user.first_name = name
        self.user.save()

    @property
    def last_name(self):
        return self.user.last_name

    @last_name.setter
    def last_name(self, last_name):
        self.user.last_name = last_name
        self.user.save()

    def __str__(self):
        return self.user.username


class Account(models.Model):
    BETA_TESTER = 1
    STUDENT = 2
    PROFESSIONAL = 3

    MEMBER_TYPES = (
        (BETA_TESTER, 'beta tester'),
        (STUDENT, 'student'),
        (PROFESSIONAL, 'professional')
    )

    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    api_key = models.CharField(max_length=250, null=False, unique=True)
    member_type = models.PositiveIntegerField(choices=MEMBER_TYPES, default=BETA_TESTER)

    def make_api_key(self, timestamp):
        key_salt = SECRET_KEY
        ts_b36 = six.text_type(int_to_base36(timestamp))
        value = (six.text_type(self.user.pk) + self.user.password + ts_b36)
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return ts_b36 + '-' + hash

    def renew_api_key(self):
        timestamp = int(datetime.utcnow().timestamp())
        self.api_key = self.make_api_key(timestamp)

    def check_api_key(self, api_key):
        ts_b36, hash = api_key.split('-')
        timestamp = base36_to_int(ts_b36)
        if not constant_time_compare(self.make_api_key(timestamp), api_key):
            return False
        return True

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.renew_api_key()

        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()

def create_account(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        user_account = Account(user=user)
        user_account.save()


post_save.connect(create_profile, sender=User)
post_save.connect(create_account, sender=User)