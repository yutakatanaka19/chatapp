from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, ResetPasswordKeyForm
from .models import CustomUser, Message

class BaseCustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['autocomplete'] = 'off'
            field.widget.attrs['placeholder'] = ''

class CustomLoginForm(BaseCustomForm, LoginForm):
    pass

class CustomSignupForm(BaseCustomForm, SignupForm):
    profile_picture = forms.ImageField(required=True)

    def save(self, request):
        user = super().save(request)
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.save()
        return user

class CustomResetPasswordForm(BaseCustomForm, ResetPasswordForm):
    pass

class CustomResetPasswordKeyForm(BaseCustomForm, ResetPasswordKeyForm):
    pass

"""
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
"""

class SearchForm(forms.Form):
    entered_text = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entered_text'].widget.attrs['autocomplete'] = 'off'
        self.fields['entered_text'].widget.attrs['placeholder'] = 'ユーザー名で検索'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['autocomplete'] = 'off'

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