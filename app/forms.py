from django import forms
from .models import UserProfile  # ✅ Rename import

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # ✅ Updated model reference
        fields = ['username', 'email', 'profile_image', 'bio', 'name']
