from django.shortcuts import render

def home(request):
    context = {
        "title": "Django Shop",
        "welcome_message": "Welcome to my Django shop from template!",
    }
    return render(request, "home.html", context)
