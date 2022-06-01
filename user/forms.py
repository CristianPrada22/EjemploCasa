from django import forms
from user.models import Person
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class SignupForm(forms.Form):
    """Sign up form."""

    username = forms.CharField(label = _('Username'), min_length=4, max_length=50)

    password = forms.CharField(
        label = _('Password'), 
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        label = _('Password confirmation'), 
        max_length=70,
        widget=forms.PasswordInput()
    )

    # first_name = forms.CharField(label = _('First name'), min_length=2, max_length=50)
    # last_name = forms.CharField(label = _('Last name'), min_length=2, max_length=50)

    email = forms.CharField(
        label = _('Email'), 
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError(_('Username is already in use.'))
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError(_('Passwords do not match.'))

        return data

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Person(user=user)
        profile.save()

