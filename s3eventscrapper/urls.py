"""
s3eventscrapper URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from urllib.parse import urlparse

import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='djangodemo API')

urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^docs/$', schema_view),
    url(r'^{}(?P<path>.*)$'.format(
        urlparse(settings.STATIC_URL).path.lstrip('/')
    ), serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^s3pooler/', include('s3pooler.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

