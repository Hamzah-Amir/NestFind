from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def about(request):
    return HttpResponse("<h1>This is about page</h1>")

def contact(request):
    return HttpResponse("<h1>This is contact page</h1>")

def blog(request):
    return HttpResponse("<h1>This is blog page</h1>")

def help(request):
    return HttpResponse("<h1>This is help page</h1>")