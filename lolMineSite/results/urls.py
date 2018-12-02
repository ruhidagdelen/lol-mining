from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('howto/', views.how_to, name='how_to'),
    path('results/', views.results, name='resutls')
]