from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import UserProfile
from registration.forms import RegistrationForm

class UserProfileForm(RegistrationForm):
    username        = forms.CharField(max_length=100)
    email           = forms.EmailField()
    #first_name      = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())



    class Meta:
        model = UserProfile
        fields = ('username','email', 'picture','password1','password2')
    def clean_username(self):
                username = self.cleaned_data['username']
                try:
                        User.objects.get(username=username)
                except User.DoesNotExist:
                        return username
                raise forms.ValidationError( username + " is already taken, please enter another.")

    def clean_email(self):
                email = self.cleaned_data['email']
                try:
                        User.objects.get(email=email)
                except User.DoesNotExist:
                        return email
                raise forms.ValidationError( email + " is already taken, please enter another.")


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
