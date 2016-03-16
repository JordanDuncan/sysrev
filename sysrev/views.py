from django.shortcuts import render

# Create your views here.

def dashboard(request):
    context_dict = { "page_title" : "Dashboard" }
    return render(request, "index.html", context_dict)