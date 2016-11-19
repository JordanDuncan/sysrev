from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from sysrev.forms import UserForm, UserProfileForm

from sysrev.biopy.get_data import run_query
from sysrev.models import Paper
from sysrev.models import Query, Researcher, Review, SavedQuery



def dashboard(request):
    context_dict = { "page_title" : "Dashboard" }
    
    context_dict['new_results'] = []
    # Get all saved queries
    # sq = SavedQuery.objects.filter(researcher=request.user.researcher)
    # for q in sq:
    #     new_query = {
    #         "queryID" : q.queryID.queryID,
    #         "queryString" : q.queryID.queryString,
    #         "paperCount" : 0
    #     }
    #     reviews = Review.objects.filter(query=q.queryID)
    #     for r in reviews:
    #         if r.time_stamp > request.user.researcher.lastViewed:
    #             new_query['paperCount'] += 1

    #     if new_query['paperCount'] != 0:
    #         context_dict['new_results'].append(new_query)

    # Create recent review activity
    # recent_reviews = []

    # r_r = Review.objects.all().reverse()[:5]
    # for r in r_r:
    #     try:
    #         ret = {}
    #         ret['relevant'] = r.relevant
    #         ret['query'] = r.query.queryString
    #         ret['name'] = r.researcher.user.first_name + ' ' + r.researcher.user.last_name
    #         ret['picture'] = r.researcher.picture
    #         ret['title'] = r.paperID.title
    #         recent_reviews.append(ret)
    #     except:
    #         print 'nope'

    # context_dict['recent_reviews'] = recent_reviews

    # Get recent queries
   
    context_dict['recent_queries'] = []
    
    # user_queries = SavedQuery.objects.filter(researcher=request.user.researcher)
    # relevant = []
    # for query in user_queries:
    #     reviews = Review.objects.filter(query=query.queryID, relevant=True)
    #     for review in reviews:

    #         if review.time_stamp > request.user.researcher.lastViewed:
    #             relevant.append(review)
                
    context_dict['new_relevant_reviews'] = ''            
    # request.user.researcher.lastViewed = datetime.datetime.now()
    return render(request, "index.html", context_dict)

# @auth
# def profile(request):
#     context_dict = { "page_title" : "Profile" }
#     return render(request, "profile.html", context_dict)

# @auth
# def edit(request):
#     edited = False

#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()

#             user.set_password(user.password)
#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user

#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']

#             profile.save()

#             edited = True

#         else:
#             print user_form.errors, profile_form.errors

#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()

#     return render(request,
#             'edit.html',
#             {'user_form': user_form, 'profile_form': profile_form, 'edited': edited} )


# @auth
# def newSearch(request):
#     if request.method == 'POST':
#         query = request.POST.get('query')

#         if query:
#             # check to see if this query exists
#             if len(Query.objects.filter(queryString__iexact=query)) != 0:
#                 prev_query = Query.objects.get(queryString=query)
#                 #return HttpResponse('query already saved (redirect to results for that query)')
#                 return HttpResponse('{"queryID":'+str(prev_query.queryID)+'}')

#             result_list = run_query(query)
#             obtained_ids = result_list.keys()
#             new_query = Query(queryString=query, result=obtained_ids, poolSize=20, researcher=request.user.researcher)
#             new_query.save()

#             n = 0
#             for key, item in result_list.iteritems():
#                 if item['Date_completed'] == 'incomplete':
#                     new_paper = Paper(paperID=key,
#                                       paperUrl=item['Link'],
#                                       authors=item['Authors'],
#                                       title=item['Article_title'],
#                                       abstract=item['Abstract'],
#                                       queryID=new_query,
#                                       abstractApproved=False,
#                                       documentApproved=False
#                                       )
#                 elif item['Date_completed'] == '':
#                     new_paper = Paper(paperID=key,
#                                       paperUrl=item['Link'],
#                                       authors=item['Authors'],
#                                       title=item['Article_title'],
#                                       abstract=item['Abstract'],
#                                       queryID=new_query,
#                                       abstractApproved=False,
#                                       documentApproved=False
#                                       )
#                 else:
#                     new_paper = Paper(paperID=key,
#                                       paperUrl=item['Link'],
#                                       authors=item['Authors'],
#                                       title=item['Article_title'],
#                                       publishDate=item['Date_completed'],
#                                       abstract=item['Abstract'],
#                                       queryID=new_query,
#                                       abstractApproved=False,
#                                       documentApproved=False
#                                       )
#                 new_paper.save()
#                 n += 1

#             #return HttpResponse('query saved')
#             return HttpResponse('{"queryID":'+str(new_query.queryID)+'}')

#     context_dict = {"page_title": "Searches"}

#     query_list = SavedQuery.objects.filter(researcher=request.user.researcher).reverse()
#     saved_list = []

#     for q in query_list:
#         sl = { 'query' : q.queryID }
#         sl['size'] = len(Paper.objects.filter(queryID=q.queryID, documentApproved=True))
#         saved_list.append(sl)

#     context_dict['saved_list'] = saved_list

#     return render(request, "newSearch.html", context_dict)

# @auth
# def searchResults(request, query_id):
#     context_dict = {"page_title": "Search Results"}
#     try:
#         query = Query.objects.get(queryID=query_id)
#     except Query.DoesNotExist:
#         raise Http404("Query does not exist")

#     if query:
#         result_list = Paper.objects.filter(queryID=query, documentApproved=True)

#         context_dict['status'] = "Query found"
#         context_dict['query'] = query
#         context_dict['result_list'] = result_list

#         # check if the user has saved the query
#         context_dict['saved'] = True
#         try:
#             sq = SavedQuery.objects.get(
#                 queryID=query,
#                 researcher=request.user.researcher
#             )
#         except SavedQuery.DoesNotExist:
#             context_dict['saved'] = False
#     else:
#         context_dict['status'] = "No such Query found"
#     return render(request, "searchResults.html", context_dict)

# @auth
# def review(request):
#     context_dict = { "page_title" : "Review", "saved_queries" : [] }

#     sq = SavedQuery.objects.filter(researcher=request.user.researcher)

#     for q in sq:
#         context_dict['saved_queries'].append(q.queryID)

#     return render(request, "review.html", context_dict)

# def ajax_review(request):
#     if request.method == "GET":
#         queryID = request.GET.get('queryID')
#         type = request.GET.get('type')

#         if queryID:
#             if type:
#                 if type == "document":
#                     paper = Paper.objects.filter(queryID__queryID=queryID, abstractApproved=True, documentApproved=False).order_by('?').first()
#                 elif type == "abstract":
#                     paper = Paper.objects.filter(queryID__queryID=queryID, abstractApproved=False, documentApproved=False).order_by('?').first()
#                 else:
#                     return JsonResponse({"status" : "error", "error" : "type incorrect"})

#                 if paper:
#                     paper_return = {
#                         "paperID" : paper.paperID,
#                         "title" : paper.title,
#                         "queryID" : paper.queryID.queryID,
#                         "queryString" : paper.queryID.queryString,
#                     }

#                     if paper.abstractApproved == False:
#                         paper_return['abstract'] = paper.abstract
#                     else:
#                         paper_return['paperUrl'] = paper.paperUrl

#                     return JsonResponse(paper_return)
#                 else:
#                     return JsonResponse({"status" : "error", "error" : "No Papers."})
#         else:
#             return JsonResponse({"status" : "error", "error" : "queryID not set"})

#     elif request.method == "POST":
#         paperID = request.POST.get('paperID')
#         relevantStr = request.POST.get('relevant')
#         notes = request.POST.get('notes')

#         relevant = False

#         if relevantStr:
#             if relevantStr == "1":
#                 relevant = True
#             elif relevantStr == "0":
#                 relevant = False
#         else:
#             return JsonResponse({"status" : "error", "error" : "relevant post parameter not set or incorrect"})

#         if not notes:
#             notes = ""

#         if paperID:
#             # get paper
#             try:
#                 paper = Paper.objects.get(paperID=paperID)
#             except Paper.DoesNotExist:
#                 raise JsonResponse({"status" : "error", "error" : "Paper does not exist."})

#             # if abstract review stage, abstractApproved, else documentApproved and create new Review object
#             if paper.abstractApproved == False:
#                 if not relevant:
#                     paper.delete()
#                     return JsonResponse({"status" : "success"})

#                 paper.abstractApproved = True

#             else:
#                 paper.documentApproved = True

#                 # create review
#                 r = Review(
#                     paperID=paper,
#                     researcher=request.user.researcher,
#                     query=paper.queryID,
#                     relevant=relevant,
#                     notes=notes
#                 )
#                 r.save()

#             paper.save()

#             return JsonResponse({"status" : "success"})

#         else:
#             return JsonResponse({"status" : "error", "error" : "paperID post parameter not set or incorrect"})

# @auth
# def ajax_saveQuery(request):
#     if request.method == "POST":
#         queryID = request.POST.get('queryID')

#         if queryID:
#             #Check if query id is valid
#             try:
#                 query = Query.objects.get(queryID=queryID)
#             except Query.DoesNotExist:
#                 raise JsonResponse({"status" : "error", "error" : "Query does not exist."})

#             try:
#                 sq = SavedQuery.objects.get(
#                     queryID=query,
#                     researcher=request.user.researcher
#                 )
#             except SavedQuery.DoesNotExist:
#                 sq = SavedQuery(
#                     queryID=query,
#                     researcher=request.user.researcher
#                 )
#                 sq.save()

#                 return JsonResponse({"status" : "success", "set" : True})

#             sq.delete()
#             return JsonResponse({"status" : "success", "set" : False})

#         else:
#             return JsonResponse({"status" : "error", "error" : "queryID post parameter not set or incorrect"})