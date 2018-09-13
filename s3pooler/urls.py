from django.conf.urls import url
from . import views


urlpatterns = [
    url('settime/pooler', views.set_s3pooler_datetime),
    url('settime/visions', views.set_visions_datetime),
    url('delete_paths', views.delete_paths),
]
