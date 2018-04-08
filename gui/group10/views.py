from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'group10/form.html')


def search(request):
    if request.method == 'POST':
        result = "Mock Result"
        try:
            # do something with user
            html = result
            return HttpResponse(html)
        except:
            return HttpResponse("no such user")
    else:
        return render(request, 'group10/form.html')
