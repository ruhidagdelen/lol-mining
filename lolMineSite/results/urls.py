from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'results'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^how_to/$', views.how_to, name="how_to"),
    url(r'^results/$', views.results, name="results")
]