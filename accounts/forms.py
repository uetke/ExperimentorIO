from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    def save(self, commit=True):
        model_instance = super(ProfileUpdateForm, self).save(commit=False)
        model_instance.first_name = self.cleaned_data['first_name']
        model_instance.save()
        return model_instance

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'github_account', 'twitter_username',
                  'website', 'workplace', 'public']

        help_texts = {
            'public': 'Make your profile available to other logged in users',
            'bio': 'You can use markdown to style your profile'
        }

        widgets = {
            'public': forms.CheckboxInput(attrs={'data-toggle': 'toggle', 'class': 'switch'}),
            'bio': forms.Textarea(attrs={'rows': 4})
        }


