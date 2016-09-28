from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie.api import NamespacedApi

from api import *

v1_api = NamespacedApi(api_name='v1',urlconf_namespace='mysite')
v1_api.register(BookResource())
v1_api.register(GenreResource())
v1_api.register(AuthorResource())
v1_api.register(PublisherResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)), 
)
