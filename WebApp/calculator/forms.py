from django import forms
from django.contrib.auth.models import User
from .models import *

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm,PasswordResetForm

class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'name': 'username', 'placeholder': 'Username'}),max_length=50, required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'name': 'first_name', 'placeholder': 'First name'}), max_length=50, required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'name': 'last_name', 'placeholder': 'Last name'}),
        max_length=50, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'password1', 'placeholder': 'Password'}),
                                max_length=100,required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'password2', 'placeholder': 'Confirm Password'}),
                                max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2']

    def clean_username(self):
        try:
            username = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data




class LoginForm(forms.Form):
    username= forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'name': 'username', 'placeholder': 'Username'}),
        error_messages=dict(invalid="Enter a valid username"),max_length=100,required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'password1', 'placeholder': 'Password'}),max_length=100, required=True)

    class Meta:
        fields = ['username','password1']

    def clean_username(self):
        try:
            username = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            raise forms.ValidationError(_("The username does not exist."))
        return self.cleaned_data['username']


class CalculatorForm(forms.ModelForm):
    expression = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'name': 'expression'}),max_length=300, required=True)

    class Meta:
        model = History
        fields = ['expression']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
