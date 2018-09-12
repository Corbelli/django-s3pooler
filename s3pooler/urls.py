from django.conf.urls import url
from . import views


urlpatterns = [
    url('scrapp', views.set_scrapping_datetime),
    url('delete_paths', views.delete_paths),
]
