from django.forms import ModelForm

from experimentor.models import Experiment, Signal


class NewExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        fields = ['name', 'visibility', 'description']


class NewSignalForm(ModelForm):
    class Meta:
        model = Signal
        fields = '__all__'
        exclude = ['experiment', 'slug']