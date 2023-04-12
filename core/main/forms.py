from django import forms
from django.core.exceptions import ValidationError

def contains_digit(password):
    pass

class RegistrationForm(forms.Form):
    username = forms.CharField(label="User Name")
    
    password1 = forms.CharField(
        label='password1',
        widget=forms.PasswordInput,
        validators=[contains_digit]
    )
    
    password2 = forms.CharField(
        label='password2',
        widget=forms.PasswordInput,
        validators=[contains_digit]
    )
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch Or None ')
        
        
        if len(password1) < 8:
            raise forms.ValidationError('Password mismatch Or None ')
        
        contains_digit(password1)
        
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        
        contains_digit(password1)
        
        return cleaned_data
