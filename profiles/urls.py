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
from profiles import views

# Examples:
# GET /profiles/overview/
# GET /profiles/overview/1/
# GET /profiles/1/overview/1/
# GET /profiles/1/days/1

# Define the namespace for `profiles` app
app_name = "profiles"

# Define the URL patterns for the `profiles` app
urlpatterns = [

    # Index
    path(route='',
         view=views.index,
         name='index'),

    path(route='overview/',
         view=views.get_overall_overview,
         name='get_overall_overview'
         ),

    path(route='overview/<int:day_id>/',
         view=views.get_day_overview,
         name='get_day_overview'
         ),

    # Overview Endpoints
    path(route='<int:profile_id>/overview/<int:day_id>/',
         view=views.get_profile_overview,
         name='get_profile_overview'
         ),

    # Daily Status Endpoints
    path(route='<int:profile_id>/days/<int:day_id>/',
         view=views.get_day_data,
         name='get_day_data'
         ),

    path(route='logs/',
         view=views.get_logs,
         name='get_logs'
         ),

    # Configuration Endpoints
    path(route='config/',
         view=views.handle_config,
         name='handle_config'
         ),

]
