from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'results'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^how_to/$', views.how_to, name="how_to"),
    # url(r'^results/$', views.results, name="results")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)