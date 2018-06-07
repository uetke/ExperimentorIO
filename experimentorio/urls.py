"""experimentorio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from experimentor import views as exp_views
from experimentor.views import index, experiment_view, new_experiment, new_signal, signal_view, experiments_view
from accounts.views import AccountView, SignUp, LoginView, profile_view

from api.urls import urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignUp.as_view(), name='signup'),
    path('u/<str:username>', AccountView.as_view(), name='account'),
    path('u/<str:username>/profile', profile_view, name='profile'),
    path('u/<str:username>/experiments', experiments_view, name='experiments'),
    path('u/<str:username>/experiment/<str:experiment_slug>', experiment_view, name='experiment'),
    path('u/<str:username>/experiment/<str:experiment_slug>/signal/new', new_signal, name='new_signal'),
    path('u/<str:username>/<str:experiment_slug>/<str:signal_slug>', signal_view, name='signal'),
    path('experiment/new', new_experiment, name='new_experiment'),
    path('api/', include('api.urls'), name='api'),
]
