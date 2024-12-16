from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Crime Analysis Map!")

def crimemap_view(request):
    return render(request, 'crimemap.html')

