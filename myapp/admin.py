from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Message

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'password', 'profile_picture', 'first_name', 'last_name', 'id', 'is_staff']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'text', 'created_at']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Message, MessageAdmin)