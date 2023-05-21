from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser as User
from .models import PostsModel, Comment

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


class NewPostModelForm(forms.ModelForm):
    class Meta:
        model = PostsModel
        fields = ["post_title", "post_text", "post_image"]
        
        
class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text",]
        
        
		


