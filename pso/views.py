from django.http import HttpResponseNotFound


def handler404(request,q):
    
    return HttpResponseNotFound(request,'404.html',status=404),