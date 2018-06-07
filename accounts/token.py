from django.utils.http import base36_to_int, int_to_base36
from django.utils import six
from django.utils.crypto import constant_time_compare, salted_hmac
from datetime import date


class ApiTokenGenerator:
    def make_token(self, user):
        today = date.today()
        num_days = (today - date(2001, 1, 1)).days
        ts_b36 = int_to_base36(num_days)
        key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"
        value = (six.text_type(user.pk) + user.password + six.text_type(num_days))
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)

    def check_token(self, user, token):
        try:
            ts_b36, hash = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

