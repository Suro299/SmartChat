from django import forms
from .models import ContactUs


class NewMessage(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ["message",]