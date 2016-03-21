from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from sysrev.forms import UserForm, UserProfileForm

from sysrev.biopy.get_data import run_query
from sysrev.models import Paper
from sysrev.models import Query, Researcher

# Custom login required decorator
def auth(function):
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/login/")
        else:
            return function(request, *args, **kw)
    return wrapper

def index(request):
    context_dict = { "page_title" : "Index" }
    return render(request, "login.html", context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect("/dashboard/")

        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                print user
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponse("You've been AFK, Sysrev account inactive.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect("/dashboard/")
        return render(request, 'login.html', {})

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')

@auth
def dashboard(request):
    context_dict = { "page_title" : "Dashboard" }
    return render(request, "dashboard.html", context_dict)

@auth
def newSearch(request):
    if request.method == 'POST':
        query = request.POST.get('query')

        if query:
            # check to see if this query exists
            if len(Query.objects.filter(queryString__iexact=query)) != 0:
                return HttpResponse('query already saved (redirect to results for that query)')

            result_list = run_query(query)
            obtained_ids = result_list.keys()
            new_query = Query(queryString=query,result=obtained_ids,poolSize=20,researcher=request.user.researcher)
            new_query.save()

            print new_query.queryID
            n = 0
            for key, item in result_list.iteritems():
                if item['Date_completed'] != 'incomplete':
                    published_date = item['Date_completed']
                else:
                    published_date = ''
                new_paper = Paper(paperID=key,
                                  paperUrl=item['Link'],
                                  authors=item['Authors'],
                                  title=item['Article_title'],
                                  publishDate=published_date,
                                  abstract=item['Abstract'],
                                  queryID=new_query,
                                  abstractApproved=False,
                                  documentApproved=False
                                  )
                new_paper.save()
                n +=1



            return HttpResponse('query saved')

    context_dict = { "page_title" : "Searches" }

    return render(request, "newSearch.html", context_dict)

@auth
def searchResults(request):
    context_dict = { "page_title" : "Search Results" }
    return render(request, "searchResults.html", context_dict)

@auth
def review(request):
    context_dict = { "page_title" : "Review" }
    return render(request, "review.html", context_dict)

