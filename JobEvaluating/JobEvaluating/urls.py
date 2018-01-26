from django.conf.urls import url
from django.contrib import admin
from App import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^display/', views.display),
    url(r'^about/', views.about),
    url(r'^search/', views.search),
    url(r'^analyse/', views.analyse),
]

