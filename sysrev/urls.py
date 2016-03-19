from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^dashboard/$', views.dashboard),
    url(r'^search/$', views.newSearch),
    url(r'^search/results', views.searchResults),
    url(r'^review/$', views.review),
]