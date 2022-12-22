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

class AssignWork(forms.Form):
    id = forms.IntegerField(label='ID работы')

#class RenameForm(forms.Form):
  #  name = forms.CharField(
   #                 widget=forms.TextInput(
  #                      attrs={
     #                       "type":"text",
         #                   "disabled":"true",
          #                  "style":"font-size: larger;",
           #                 "class":"group-info"
           #             }))

class RenameForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
                        attrs={
                            #"disabled":"true",
                            "style":"font-size: larger;",
                            #"class":"group-info"
                        }))