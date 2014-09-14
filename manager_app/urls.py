from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',"Accounts.views.index"),
    #url(r'^password/reset/done/$',auth_views.password_reset_done,name='password_reset_done',),
    url(
        r'^password/reset/done/$',
        auth_views.password_reset,
        {'template_name': 'registration/password_reset_form.html'},
        name='auth_password_reset',
    ),
    url(r'^users/', include('Accounts.urls'),),
    url(r'^admin/', include(admin.site.urls)),


)


if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}), )
