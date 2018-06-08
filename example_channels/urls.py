from django.urls import path

from .views import index, room

urlpatterns = [
    path('', room),
    path('room/<room_name>', room),
]

