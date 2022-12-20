from django import forms
from .models import *

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class NewUser(forms.Form):
    first_name = forms.CharField(label='Имя')
    second_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль')

class EditUser(forms.Form):
    first_name = forms.CharField(label='Имя')
    second_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль')

class NewGroup(forms.Form):
    first_name = forms.CharField(label='Имя')
    second_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль')

class AddMember(forms.Form):
    email = forms.CharField(label='Почта')


class AddTask(forms.Form):
    name = forms.CharField(label='Название')
    task_type = forms.CharField(label='Имя шаблона')