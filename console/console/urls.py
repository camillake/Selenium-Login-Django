from django.conf.urls import patterns, include, url
from django.contrib import admin
from test_login.views import DetailLog

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'console.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # homepage
    url(r'^$', 'test_login.views.activate_test', name='homepage'),
    # detail log page
    url(r'^detail/(?P<pk>\d+)/$', DetailLog.as_view(), name='log-detail'),


)
