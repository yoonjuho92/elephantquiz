from django.contrib import admin
from .models import UserChoice, UserProfile, Question, Text

admin.site.register(UserChoice)
admin.site.register(UserProfile)
admin.site.register(Text)
admin.site.register(Question)
