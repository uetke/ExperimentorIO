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
from django.urls import path, include

from django.contrib.auth.views import (LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from experimentor.views import (index,
                                experiment_view,
                                new_experiment,
                                new_signal,
                                signal_view,
                                experiments_view,
                                ExperimentView)

from accounts.views import (AccountView,
                            SignUp,
                            SignUpSuccess,
                            LoginView,
                            profile_view,
                            activate)

from api.urls import urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignUp.as_view(), name='signup'),
    path('signup/successful', SignUpSuccess.as_view(), name='signup_success'),
    path('reset', PasswordResetView.as_view(
        template_name='account/password_reset.html',
        email_template_name='account/password_reset_email.html',
        subject_template_name='account/password_reset_subject.txt'
    ),
         name='password_reset'),
    path('reset/done', PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'
    ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(
        template_name = 'account/password_reset_confirm.html'
    ),
         name='password_reset_confirm'),
    path('reset/complete', PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ),
         name='password_reset_complete'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('u/<str:username>', AccountView.as_view(), name='account'),
    path('u/<str:username>/profile', profile_view, name='profile'),
    path('u/<str:username>/experiments', experiments_view, name='experiments'),
    path('u/<str:username>/experiment/<str:experiment_slug>', experiment_view, name='experiment'),
    path('u/<str:username>/experiment/<str:experiment_slug>/signal/new', new_signal, name='new_signal'),
    path('u/<str:username>/<str:experiment_slug>/<str:signal_slug>', signal_view, name='signal'),
    path('experiment/new', new_experiment, name='new_experiment'),
    path('api/', include('api.urls'), name='api'),
    path('chat/', include('example_channels.urls')),
    # path('new_view/<username>/<experiment_slug>', ExperimentView.as_view()),
]
