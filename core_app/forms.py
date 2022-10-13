from django import forms
from .models import *

class AddAnswerForm(forms.Form):
    answer = forms.CharField(max_length='255', help_text="Введите сюда ответ", label='Ответ')

class AddRedirectForm(forms.Form):
    redirect = forms.CharField(max_length='255', help_text="Введите название задачи", label='Переадресовать на задачу')