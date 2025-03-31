import os
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
   return render(request, "../../template/index.html")


def all_listings(request):
   return HttpResponse('Returning all users')

