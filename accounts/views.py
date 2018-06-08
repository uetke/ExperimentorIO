from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import generic, View
from django.contrib import messages

from accounts.models import Profile
from accounts.token import account_activation_token
from experimentor.models import Experiment

from .forms import SignUpForm, ProfileUpdateForm

from django.contrib.auth.views import LoginView


class LoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return redirect('account', form.cleaned_data['username'])


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('signup_success')
    template_name = 'signup.html'

class SignUpSuccess(generic.TemplateView):
    template_name = 'account/signup_success.html'

class AccountView(LoginRequiredMixin, View):
    context_object_name = 'experiments'
    template_name = 'account/account.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get('username'))
        profile = get_object_or_404(Profile, user=user)
        if user == request.user or profile.public:
            experiments = Experiment.objects.filter(owner=user).order_by('-update_date')[:5]
            return render(request, self.template_name, {self.context_object_name: experiments})

        return redirect('home')


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'GET':
        form = ProfileUpdateForm(initial={
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'bio': profile.bio,
            'github_account': profile.github_account,
            'twitter_username': profile.twitter_username,
            'website': profile.website,
            'workplace': profile.workplace,
            'public': profile.public,
        })

        if request.user == user:
            return render(request, 'account/profile.html', {'form': form})
        elif profile.public:
            return render(request, 'account/profile_public.html', {'form': form})
        else:
            reason = 'This profile is private'
            return render(request, 'no_access.html', {'reason': reason})

    if request.method == 'POST':
        if not user == request.user:
            reason = 'You are trying to change a profile that is not yours.<br />' \
                     'This incident will be reported.'
            return render(request, 'no_access.html', {'reason': reason})

        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            profile.bio = form.cleaned_data['bio']
            profile.github_account = form.cleaned_data['github_account']
            profile.twitter_username = form.cleaned_data['twitter_username']
            profile.website = form.cleaned_data['website']
            profile.workplace = form.cleaned_data['workplace']
            profile.public = form.cleaned_data['public']
            profile.save()
            messages.success(request, 'Profile Updated')

            return redirect('profile', username=user.username)
        else:

            return render(request, 'account/profile.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.verified_email = True
        user.profile.save()
        user.save()
        messages.success(request, 'Email verified')
        return redirect('home')
    else:
        return render(request, 'account/activation_invalid.html')