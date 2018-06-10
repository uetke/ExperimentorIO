import channels.layers
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from asgiref.sync import async_to_sync


class Experiment(models.Model):
    PRIVATE = 1
    PUBLIC = 2
    VISIBILITY_CHOICES = (
        (PRIVATE, 'private'),
        (PUBLIC, 'public')
    )

    RUNNING = 1
    STOPPED = 2
    FINISHED = 3
    PAUSED = 4

    STATUS_CHOICES = (
        (RUNNING, 'running'),
        (STOPPED, 'stopped'),
        (FINISHED, 'finished'),
        (PAUSED, 'paused')
    )

    STATUS_TAGS = {
        RUNNING: 'success',
        STOPPED: 'secondary',
        FINISHED: 'info',
        PAUSED: 'light'
    }

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiments', null=False)
    name = models.CharField(max_length=140, blank=False, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES, default=PUBLIC)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=STOPPED, validators=[MaxValueValidator(4)])
    slug = models.CharField(max_length=140, null=True)

    # def get_absolute_url(self):
    #     return reverse('experiment', kwargs={'username': self.owner.username, 'experiment_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.name)
            base_slug = slugify(self.name)
            i = 1
            while Experiment.objects.filter(owner=self.owner, slug=new_slug).exists():
                new_slug = base_slug + '-{}'.format(i)
                i += 1
            self.slug = new_slug

        valid_status = [s[0] for s in self.STATUS_CHOICES]
        if self.status not in valid_status:
            raise ValueError('Status {} is not valid'.format(self.status))
        super(Experiment, self).save(*args, **kwargs)

    @property
    def status_tag(self):
        return self.STATUS_TAGS[self.status]

    @classmethod
    def get_from_user_slug(cls, username, slug):
        user = User.objects.get(username=username)
        return cls.objects.get(owner=user, slug=slug)

    def __str__(self):
        if self.slug:
            return self.slug
        return self.name


class Signal(models.Model):
    STRING = 1
    BOOL = 2
    FLOAT = 3
    INTEGER = 4
    STATUS = 5
    ARRAY = 6  # 1D Array
    ARRAY2 = 7  # 2D Array

    TYPE_CHOICES = (
        (STRING, 'string'),
        (BOOL, 'bool'),
        (FLOAT, 'float'),
        (INTEGER, 'integer'),
        (STATUS, 'status'),
        (ARRAY, '1D array'),
        (ARRAY2, '2D array')
    )

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='signals', null=False)
    name = models.CharField(max_length=140, null=False, blank=False)
    value_type = models.PositiveIntegerField(choices=TYPE_CHOICES, default=STRING)
    updated_time = models.DateTimeField(auto_now_add=True)
    units = models.CharField(max_length=10, blank=True, default='')
    slug = models.CharField(max_length=140, null=True)

    @property
    def last_value(self):
        if self.measurements.last():
            return '{} {}'.format(self.measurements.last().value, self.units)
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.name)
            base_slug = slugify(self.name)
            i = 1
            while Signal.objects.filter(experiment=self.experiment, slug=new_slug).exists():
                new_slug = base_slug + '-{}'.format(i)
                i += 1
            self.slug = new_slug
        super(Signal, self).save(*args, **kwargs)
        self.experiment.update_date = self.updated_time
        self.experiment.save()

    @classmethod
    def get_from_user_experiment_slug(cls, username, experiment_slug, slug):
        user = User.objects.get(username=username)
        experiment = Experiment.objects.get(owner=user, slug=experiment_slug)
        return cls.objects.get(experiment=experiment, slug=slug)

    def __str__(self):
        if self.slug:
            return self.slug
        return self.name


class Measurement(models.Model):
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='measurements', null=False)
    value = models.TextField(blank=False)
    updated_time = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        super(Measurement, self).save(*args, **kwargs)
        self.signal.updated_time = self.updated_time
        self.signal.save()
        channel_layer = channels.layers.get_channel_layer()
        data = {'type': 'chat_message',
                'y': self.value,
                'x': self.updated_time.timestamp()*1000}
        async_to_sync(channel_layer.group_send)("chat_aqui", data)


def last_update(sender, *args, **kwargs):
    if kwargs['created']:
        sender.signal.updated_time = now()
        sender.save()

# post_save.connect(last_update, sender=Measurement)
