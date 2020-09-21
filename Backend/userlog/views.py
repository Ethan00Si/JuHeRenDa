from django.shortcuts import render
from django.shortcuts import HttpResponse
import json

def index(request):
    user_log = request.GET
    print(user_log)
    return HttpResponse('hello app3')