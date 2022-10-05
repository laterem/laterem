from django.http import HttpResponse
from django.shortcuts import render

def Resp(request):
    return HttpResponse("Страница задания 1.1")
