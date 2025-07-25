from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Section(models.Model):
    name = models.CharField(max_length=100)  # Example: Full Stack, Python, ML
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