from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from sms import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uninotify.views.home', name='home'),
    # url(r'^uninotify/', include('uninotify.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^sms/',views.SELECT),
    url(r'^search/(\d+)*',views.SEARCH),
    url(r'^zhanshi/',views.LIULIANG),
)
