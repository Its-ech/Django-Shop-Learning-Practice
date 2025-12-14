from django.shortcuts import render

def home(request):
    context = {
        "title": "Django Shop",
        "welcome_message": "Welcome to my Django shop from template!",
        "tagline": "learning Django step by step",
    }
    return render(request, "store/home.html", context)
