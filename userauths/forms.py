from userauths.models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}), required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Location'}), required=False)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bio'}), required=False)
    url = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'URL'}), required=False)

    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'location', 'bio', 'url']


class UserRegisterationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'prompt srch_explore', 'placeholder': 'username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'prompt srch_explore', 'placeholder': 'Email'}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'prompt srch_explore', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'prompt srch_explore', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

