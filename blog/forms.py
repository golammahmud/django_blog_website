from django import forms

from .models import Post,Contact


class post(forms.ModelForm):
    class Meta:
        model=Post
        fields='__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields='__all__'