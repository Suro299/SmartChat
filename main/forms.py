from django import forms
from .models import PostsModel, Comment


class NewPostModelForm(forms.ModelForm):
    class Meta:
        model = PostsModel
        fields = ["post_title", "post_text", "post_image"]
        
        
class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text",]
        
        
		


