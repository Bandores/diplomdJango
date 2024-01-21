from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
class CustomSignupForm(UserCreationForm):
    # Переопределение меток полей
    username = forms.CharField(label=_('Имя пользователя'))
    password1 = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Подтверждение пароля'), widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
class LoginForm(forms.Form):
    username = forms.CharField(label=_('Имя пользователя'))
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)