from rest_framework import serializers
from experimentor.models import Experiment, Signal, Measurement


class ExperimentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Experiment
        fields = ('owner', 'name', 'description', 'slug')


class SignalSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='experiment.owner.username')
    experiment = serializers.ReadOnlyField(source='experiment.slug')
    class Meta:
        model = Signal
        fields = ('owner', 'experiment', 'name', 'value_type', 'updated_time', 'units', 'slug')


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('value', 'updated_time', 'expiration')