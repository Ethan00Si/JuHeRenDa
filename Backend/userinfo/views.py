from django.shortcuts import render
from django.shortcuts import HttpResponse
import json

def index(request):
    user_info = request.GET
    print(user_info)
    return HttpResponse('hello app2')