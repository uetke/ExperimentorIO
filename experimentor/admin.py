from django.contrib import admin

from experimentor.models import Experiment, Signal, Measurement


admin.site.register(Experiment)
admin.site.register(Signal)
admin.site.register(Measurement)