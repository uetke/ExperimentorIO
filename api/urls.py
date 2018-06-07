from django.urls import path

from .views import ExperimentDetail, SignalDetail, MeasurementListCreate

urlpatterns = [
    path('experiment/<pk>', ExperimentDetail.as_view(), name='experiment_detail'),
    path('signal/<pk>', SignalDetail.as_view(), name='signal_detail'),
    path('<experiment_slug>/<signal_slug>', MeasurementListCreate.as_view(), name='measurement_list'),
]

