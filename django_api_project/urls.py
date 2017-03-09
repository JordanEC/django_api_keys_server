"""django_api_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from api_keys_server import views

urlpatterns = [
    url(r'^', include('authentication.urls')),
    #url(r'^api_keys/(?P<message>[-\w]+)/$',views.APIKeyList.as_view(),name='api-keylist'),
    url(r'^api_keys/$',views.APIKeyList.as_view()),
    url(r'^api/find_duplicates/$', views.WordsDuplicatedDetail.as_view()),
    url(r'^api/$', views.api_view, name='api'),
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
]
