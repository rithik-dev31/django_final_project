from django.contrib import admin

from .models import UserProfile, Section, Post, Community, ChatMessage,JobOpening,Repolink,Feedback

# Register your models here
admin.site.register(UserProfile)
admin.site.register(Section)
admin.site.register(Post)
admin.site.register(Community)
admin.site.register(ChatMessage)
admin.site.register(JobOpening)  # Register job openings model
admin.site.register(Repolink)  # Register repo link model
admin.site.register(Feedback)  # Register feedback model