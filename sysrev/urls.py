from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^dashboard/', views.dashboard),
    url(r'^search/$', views.newSearch),
    url(r'^search/results', views.searchResults),
    url(r'^review/$', views.review),
]