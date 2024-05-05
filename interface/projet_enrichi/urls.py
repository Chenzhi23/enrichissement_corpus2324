"""projet_enrichi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from app01 import views


urlpatterns = [
    # path("admin/", admin.site.urls),
    path('', views.index),
    path('dynamique/', views.dynamique_list),
    path('act/', views.act_list),
    path('nouvelle/', views.nouvelle_list),
    path('doc/', views.doc_list),
    path('lieu/', views.lieu_list),
    path('perc/', views.perc_list),
    path('temps/', views.temps_list),
    path('simple/', views.simple_list)
]
