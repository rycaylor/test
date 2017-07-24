from django.conf.urls import url
from . import views
# from django.contrib import admin
app_name = 'belt'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^add$', views.add, name = 'add'),
    url(r'^make_cat$', views.make_cat, name = 'make_cat'),
    url(r'^like/(?P<id>\d+)$', views.like, name = 'like'),
    url(r'^unlike/(?P<id>\d+)$', views.unlike, name = 'unlike'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name = 'delete'),
    url(r'^info/(?P<id>\d+)$', views.info, name = 'info'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name = 'edit'),
    url(r'^change/$', views.change, name = 'change'),

]
