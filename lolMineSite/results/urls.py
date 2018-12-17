from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'results'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^about/$', views.about, name='about'),
    url(r'^how_it_works/$', views.how_to, name="how_it_works"),
    # url(r'^results/$', views.results, name="results"),
    url(r'^not_found/$', views.not_found, name="not_found"),
    url(r'^criteria/$', views.criteria, name="criteria")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)