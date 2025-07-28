from django.contrib import admin

from .models import UserProfile, Section, Post, Community, ChatMessage

# Register your models here
admin.site.register(UserProfile)
admin.site.register(Section)
admin.site.register(Post)
admin.site.register(Community)
admin.site.register(ChatMessage)
