from http.client import HTTPResponse
from django.shortcuts import render

def Resp(request):
    return HTTPResponse("Страница задания 1.1")
