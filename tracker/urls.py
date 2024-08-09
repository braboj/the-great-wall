"""
URL configuration for project project.

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
# from django.contrib import admin
from django.urls import path
from django.contrib import admin
from tracker import views

urlpatterns = [
    path('overview/', views.total_cost, name='total_cost'),
    path('overview/<int:day_id>/', views.daily_cost, name='daily_cost'),
    path('<int:profile_id>/overview/<int:day_id>/', views.daily_profile_cost,
         name='daily_profile_cost'),
    path('<int:profile_id>/days/<int:day_id>/', views.profile_daily_details,
         name='profile_day_detail'),
]


# GET /profiles/overview/
# GET /profiles/overview/1/
# GET /profiles/1/overview/1/
# GET /profiles/1/days/1
