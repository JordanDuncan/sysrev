from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^dashboard/', views.dashboard),
    url(r'^search/$', views.newSearch),
    url(r'^search/([0-9])/$', views.searchResults),
    url(r'^review/$', views.review),

    url(r'^ajax/review/$', views.ajax_review),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)