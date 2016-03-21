from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import datetime
from sysrev.forms import UserForm, UserProfileForm

from sysrev.biopy.get_data import run_query
from sysrev.models import Paper
from sysrev.models import Query, Researcher, Review

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
    request.user.researcher.lastViewed = datetime.datetime.now()

    # Create recent review activity
    recent_reviews = []

    r_r = Review.objects.all().reverse()[:5]
    for r in r_r:
        try:
            ret = {}
            ret['relevant'] = r.relevant
            ret['query'] = r.query.queryString
            ret['name'] = r.researcher.user.first_name + ' ' + r.researcher.user.last_name
            ret['picture'] = r.researcher.picture
            ret['title'] = r.paperID.title
            recent_reviews.append(ret)
        except:
            print 'nope'

    context_dict['recent_reviews'] = recent_reviews

    # Get recent queries
    recent_queries = Query.objects.filter().reverse()[:10]

    context_dict['recent_queries'] = recent_queries
    
    user_queries = Query.objects.filter(researcher=request.user.researcher)
    relevant = []
    for query in user_queries:
        reviews = Review.objects.filter(query=query, relevant=True)
        for review in reviews:
            if review.time_stamp > request.user.researcher.lastViewed:
                relevant.append(review)
                
    context_dict['new_relevant_reviews'] = relevant            
    request.user.researcher.lastViewed = datetime.datetime.now()
    return render(request, "dashboard.html", context_dict)

@auth
def newSearch(request):
    if request.method == 'POST':
        query = request.POST.get('query')

        if query:
            # check to see if this query exists
            if len(Query.objects.filter(queryString__iexact=query)) != 0:
                prev_query = Query.objects.get(queryString=query)
                #return HttpResponse('query already saved (redirect to results for that query)')
                return HttpResponse('{"queryID":'+str(prev_query.queryID)+'}')

            result_list = run_query(query)
            obtained_ids = result_list.keys()
            new_query = Query(queryString=query, result=obtained_ids, poolSize=20, researcher=request.user.researcher)
            new_query.save()

            print new_query.queryID
            n = 0
            for key, item in result_list.iteritems():
                if item['Date_completed'] == 'incomplete':
                    new_paper = Paper(paperID=key,
                                      paperUrl=item['Link'],
                                      authors=item['Authors'],
                                      title=item['Article_title'],
                                      abstract=item['Abstract'],
                                      queryID=new_query,
                                      abstractApproved=False,
                                      documentApproved=False
                                      )
                elif item['Date_completed'] == '':
                    new_paper = Paper(paperID=key,
                                      paperUrl=item['Link'],
                                      authors=item['Authors'],
                                      title=item['Article_title'],
                                      abstract=item['Abstract'],
                                      queryID=new_query,
                                      abstractApproved=False,
                                      documentApproved=False
                                      )
                else:
                    new_paper = Paper(paperID=key,
                                      paperUrl=item['Link'],
                                      authors=item['Authors'],
                                      title=item['Article_title'],
                                      publishDate=item['Date_completed'],
                                      abstract=item['Abstract'],
                                      queryID=new_query,
                                      abstractApproved=False,
                                      documentApproved=False
                                      )
                new_paper.save()
                n += 1

            #return HttpResponse('query saved')
            return HttpResponse('{"queryID":'+str(new_query.queryID)+'}')

    context_dict = {"page_title": "Searches"}

    query_list = Query.objects.filter(researcher=request.user.researcher).reverse()
    saved_list = []

    for q in query_list:
        sl = { 'query' : q }
        sl['size'] = len(Paper.objects.filter(queryID=q, documentApproved=True))
        saved_list.append(sl)

    context_dict['saved_list'] = saved_list

    return render(request, "newSearch.html", context_dict)

@auth
def searchResults(request, query_id):
    context_dict = {"page_title": "Search Results"}
    try:
        query = Query.objects.get(queryID=query_id)
    except Query.DoesNotExist:
        raise Http404("Query does not exist")


    if query:
        result_list = Paper.objects.filter(queryID=query, documentApproved=True)

        context_dict['status'] = "Query found"
        context_dict['query'] = query
        context_dict['result_list'] = result_list
    else:
        context_dict['status'] = "No such Query found"
    return render(request, "searchResults.html", context_dict)

@auth
def review(request):
    context_dict = { "page_title" : "Review" }
    from django.db import connection
    cursor = connection.cursor()

    cursor.execute("SELECT queryID FROM Query WHERE MIN(startDate) AND resolved = FALSE ")
    firstUnresolvedQuery = cursor.fetchone() #Its the first unresolved query timestamp-wise
    cursor.execute("SELECT paperID,abstract,paperUrl FROM Paper WHERE MIN(paperID) AND queryID = %s AND (documentApproved = None OR abstractApproved = None)",[firstUnresolvedQuery])
    paperObject = cursor.execute #The first paper id-wise relative to the given query that has not either abstract or paper being evaluated
    cursor.execute("SELECT queryString,description FROM Query WHERE queryID = %s",[firstUnresolvedQuery])
    queryObject = cursor.execute #The query object relative to the query
    #return render(request, "review.html", context_dict)
    return HttpResponse('{"query": %s,"paper": %s}',[queryObject],[paperObject])
