from django import forms
from .models import UserProfile  # ✅ Rename import
from .models import Post

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # ✅ Updated model reference
        fields = ['username', 'email', 'profile_image', 'bio', 'name']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['section', 'content_name', 'description', 'url']