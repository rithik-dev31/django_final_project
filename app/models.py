from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):  # ✅ Renamed to avoid conflict
    name=models.CharField(max_length=100, blank=True, null=True)  # ✅ Add this line
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.png')
    bio = models.TextField(blank=True, null=True)  # ✅ Add this line

    def __str__(self):
        return self.username

class Section(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='section_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content_name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.content_name

class Community(models.Model):
    section = models.OneToOneField(Section, on_delete=models.CASCADE, related_name='community')
    members = models.ManyToManyField(UserProfile, related_name='communities')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Community for {self.section.name}"

class ChatMessage(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"
    
# job opening section

class JobOpening(models.Model):  # ← Renamed from jobopenings
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content_name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.content_name
    

class Repolink(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=255)
    description = models.TextField()
    repo_url = models.URLField(max_length=500)

    def __str__(self):
        return self.repo_name