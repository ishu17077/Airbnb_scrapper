import os
from django.http import HttpResponse
from django.shortcuts import render
from backend.constants import dirPath
from .models import *
from django.core import serializers

# Create your views here.

def index(request):
   print(dirPath)
   return render(request, "index.html")


def all_listings(request):
   return HttpResponse('Returning all users')

def showAllListings(request):
   
   airbnbListings = AirbnbListing.objects.all()
   airbnbListingsJson = serializers.serialize("json", airbnbListings)
   return HttpResponse(
    airbnbListingsJson, content_type="application/json"
   )

def showSpecificListings(request, location:str):
    airbnbListings = AirbnbListing.objects.all()
    searchResult = []
    for airbnbListing in airbnbListings:
       if location.upper() == airbnbListing.location.upper():
          searchResult.append(airbnbListing)
    searchResult = serializers.serialize("json", searchResult)
    return HttpResponse(
     searchResult, content_type="application/json"
    ) 