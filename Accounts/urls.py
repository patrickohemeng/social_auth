from django.conf.urls import patterns, url, include
from Accounts import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^accounts/', include('registration.backends.default.urls'), name='register'),
    )