from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "profile_picture"]
        help_texts = {
            "username": None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password1'].error_messages['required'] = 'Enter your password.'
        self.fields['password2'].error_messages['required'] = 'Enter your password (for confirmation).'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]

class UsernameChangingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username"]
        labels = {"username": "New username"}
        help_texts = {
            "username": None,
        }

class EmailChangingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email"]
        labels = {"email": "New email address"}

class IconChangingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["profile_picture"]

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].help_text = None
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None