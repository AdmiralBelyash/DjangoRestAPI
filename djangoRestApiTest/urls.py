"""djangoRestApiTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from Testing import views


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/users/$', views.users_list),
    re_path(r'^api/users/(?P<pk>[0-9]+)$', views.users_detail),
    re_path(r'^api/testing/$', views.testing_list),
    re_path(r'^api/testing/(?P<pk>[0-9]+)$', views.testing_detail),
    re_path(r'^api/questions/$', views.questions_list),
    re_path(r'^api/questions/(?P<pk>[0-9]+)$', views.questions_detail),
    re_path(r'^api/themes/$', views.theme_list),
    re_path(r'^api/themes/(?P<pk>[0-9]+)$', views.theme_detail),
    re_path(r'^api/algorithm/(?P<pk>[0-9]+)$', views.test_algorithm),
    re_path(r'^api/question_theme/(?P<pk>[0-9]+)$', views.questions_theme),
]
