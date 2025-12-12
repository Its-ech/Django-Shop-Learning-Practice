from django.http import HttpResponse

def home(request):
    return HttpResponse("HELLO ECH - TEST 123")
