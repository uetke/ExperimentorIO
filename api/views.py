from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics

from accounts.models import Account
from .serializers import ExperimentSerializer, SignalSerializer, MeasurementSerializer
from .permissions import IsOwner, IsOwnerSignal
from experimentor.models import Experiment, Signal, Measurement


class ExperimentDetail(generics.RetrieveAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsOwner, )


class SignalDetail(generics.RetrieveAPIView):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    permission_classes = (IsOwnerSignal, )


class MeasurementListCreate(generics.ListCreateAPIView):
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        user = Account.objects.get(api_key=self.request.META.get('HTTP_API_KEY')).user
        experiment = Experiment.objects.get(owner=user, slug=self.kwargs['experiment_slug'])
        signal = Signal.objects.get(experiment=experiment, slug=self.kwargs['signal_slug'])
        measurements = Measurement.objects.filter(signal=signal)
        return measurements


    def perform_create(self, serializer):
        user = Account.objects.get(api_key=self.request.META.get('HTTP_API_KEY')).user
        experiment = Experiment.objects.get(owner=user, slug=self.kwargs['experiment_slug'])
        signal = Signal.objects.get(experiment=experiment, slug=self.kwargs['signal_slug'])
        serializer.save(signal=signal)
