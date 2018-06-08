import sys
from accounts.models import User

def update_size():
    for u in User.objects.all():
        s = 0
        for experiment in u.experiments.all():
            for signal in experiment.signals.all():
                for measurement in signal.measurements.all():
                    s += sys.getsizeof(measurement.value)

        u.account.data_size = s
        u.account.save()