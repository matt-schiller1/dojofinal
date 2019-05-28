from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^register', views.register),
  url(r'^dashboard', views.dashboard),
  url(r'^login', views.login),
  url(r'^addplan', views.addplan),
  url(r'^addtrip', views.addtrip),
  url(r'^logout', views.logout),
  url(r'^trips/(?P<my_val>\d+)$', views.displaytrip),
  url(r'^join/(?P<my_val>\d+)$', views.jointrip)

]