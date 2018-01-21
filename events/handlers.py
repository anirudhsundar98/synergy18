from django.shortcuts import render
from django.http import HttpResponse
def handler_404(request):
    try:
        return render(request, "404.html")
    except:
        return HttpResponse(" 404 !")