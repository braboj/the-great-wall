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
from django.urls import path, re_path
from tracker import views


# GET /profiles/overview/
# GET /profiles/overview/1/
# GET /profiles/1/overview/1/
# GET /profiles/1/days/1

urlpatterns = [
    path('overview/', views.overview_fetch, name='total_cost'),
    path('overview/<int:day_id>/', views.overview_day_fetch, name='daily_cost'),
    path('<int:profile_id>/overview/<int:day_id>/', views.overview_profile_day_fetch,
         name='daily_profile_cost'),
    path('<int:profile_id>/days/<int:day_id>/', views.daily_profile_status_fetch,
         name='profile_day_detail'),

    re_path(route=r"^((?P<profile_id>\d+)/)?overview(/(?P<day_id>\d+))?/$",
            view=views.overview_fetch
            ),
]

