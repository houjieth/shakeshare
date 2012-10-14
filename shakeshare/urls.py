from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shakeshare.views.home', name='home'),
    # url(r'^shakeshare/', include('shakeshare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^hello/$', 'shakeshare.views.hello', name='hello'),
    (r'^shakeshare/$', 'shakeshare.views.landing'),
    (r'^shakeshare/share/$', 'shakeshare.views.share'),
    (r'^shakeshare/upload/$', 'shakeshare.views.upload'),

    (r'^hello/$', 'shakeshare.views.hello'),
)
