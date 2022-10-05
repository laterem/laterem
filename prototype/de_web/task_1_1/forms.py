from django import forms
from .models import *

class AddAnswerForm(forms.Form):
    Ответ = forms.CharField(max_length='255', help_text="Введите сюда ответ")