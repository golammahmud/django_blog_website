from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# class UserRegistrationForm(UserCreationForm):
#     email=forms.EmailField()
#     First_name=forms.CharField(max_length=100)
#     Last_name=forms.CharField(max_length=100)
#     class Meta:
#         model = User
#         fields=['username', 'email','First_name','Last_name','password1','password2']

# Sign Up Form
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]
        
        
        
class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['images']