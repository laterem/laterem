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

class AddMember(forms.Form):
    email = forms.CharField(label='Почта')

class AssignWork(forms.Form):
    id = forms.IntegerField(label='ID работы')

class UploadTask(forms.Form):
    task_type_name = forms.CharField(label='Имя шаблона', max_length=128)
    config = forms.FileField(label='Файл конфигурации LTC')
    view = forms.FileField(label='Файл разметки HTML')