from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from users.models import CustomUser as User


class NewUserForm(UserCreationForm):
	email = forms.EmailField(max_length=200, help_text='Required')

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user