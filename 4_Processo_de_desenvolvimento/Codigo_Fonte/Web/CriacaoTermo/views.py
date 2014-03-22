from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Ola! Voce esta a navegar no Nzayilumbandu")

