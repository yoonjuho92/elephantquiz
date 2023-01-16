from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class UserProfileForm(forms.ModelForm):
    difficulty = forms.ChoiceField(label="난이도", choices=UserProfile.difficulty_choices, required=True)
    class Meta:
        model = UserProfile
        fields = ["difficulty"]