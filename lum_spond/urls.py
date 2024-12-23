"""
URL configuration for lum_spond project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [

    # path('', views.test, name = 'index'),

    path('', views.index, name = 'index'),
    path('user', views.userLogin, name = 'userLogin'),
    path('admin', views.adminLogin, name = 'adminLogin'),

    path('userportal', views.userportal, name = 'userportal'),
    path('adminportal', views.adminportal, name = 'adminportal'),
    path('remove/<int:pk>', views.remove, name = 'remove'),
    path('addUser', views.addUser, name='addUser'),
    path('report', views.reports, name = 'reports'),
]
