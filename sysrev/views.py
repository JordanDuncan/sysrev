from django.shortcuts import render

def login(request):
    context_dict = { "page_title" : "Login" }
    return render(request, "login.html", context_dict)

def dashboard(request):
    context_dict = { "page_title" : "Dashboard" }
    return render(request, "index.html", context_dict)

def newSearch(request):
    context_dict = { "page_title" : "Seaches" }
    return render(request, "newSearch.html", context_dict)

def searchResults(request):
    context_dict = { "page_title" : "Search Results" }
    return render(request, "searchResults.html", context_dict)

def review(request):
    context_dict = { "page_title" : "Review" }
    return render(request, "review.html", context_dict)