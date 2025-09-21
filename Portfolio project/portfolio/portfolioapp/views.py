
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "portfolioapp/index.html")   # looks for templates/index.html

def contact(request):
    return render(request, "portfolioapp/contact.html") # looks for templates/contact.html
