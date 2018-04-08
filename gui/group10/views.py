from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'group10/test2.html')
