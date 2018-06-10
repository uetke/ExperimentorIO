from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'home.html', {})

def room(request, room_name):
    return render(request, 'example_channels/plot_update.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
