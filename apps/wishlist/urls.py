from django.conf.urls import url
from . import views  
        
urlpatterns = [
url(r'^$', views.index),
url(r'^register$', views.register),
url(r'^login$', views.login),
url(r'^dashboard$', views.dashboard),
url(r'^added$', views.added),
url(r'^item/(?P<id>\d+)$', views.item),
url(r'^addWish/(?P<id>\d+)$', views.addWish),
url(r'^removeWish/(?P<id>\d+)$', views.removeWish),
url(r'^submitted$', views.submitted),
url(r'^delete/(?P<id>\d+)$', views.delete),
url(r'^logout/$', views.logout), 
]