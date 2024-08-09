from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from builder.simulator import *
from django.apps import apps

def home(request):
    return HttpResponse('Hello, World!')


def get_overall_overview(request):

    config_list = apps.get_app_config("tracker").config_list
    num_teams = apps.get_app_config("tracker").num_teams

    try:
        builder = WallManager(config_list)
        builder.build(num_teams=num_teams, days=30)

    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)})

    else:

        data = {
            'day': None,
            'cost': builder.get_cost()
        }

        return JsonResponse(data)


def get_day_overview(request, day_id):

    config_list = apps.get_app_config("tracker").config_list
    num_teams = apps.get_app_config("tracker").num_teams

    try:
        builder = WallManager(config_list)
        builder.build(num_teams=num_teams, days=day_id)

    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)})

    else:
        data = {
            'day': day_id,
            'cost': builder.get_cost()
        }

        return JsonResponse(data)


def get_profile_overview(request, profile_id, day_id):

    config_list = apps.get_app_config("tracker").config_list
    num_teams = apps.get_app_config("tracker").num_teams

    try:
        builder = WallManager(config_list)
        builder.build(num_teams=num_teams, days=day_id)
        profile = builder.profiles[profile_id-1]

    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)})

    else:
        data = {
            'day': day_id,
            'cost': profile.get_cost()
        }

        return JsonResponse(data)


def get_day_data(request, profile_id, day_id):

    config_list = apps.get_app_config("tracker").config_list
    num_teams = apps.get_app_config("tracker").num_teams

    try:
        builder = WallManager(config_list)
        builder.build(num_teams=num_teams, days=day_id)
        profile = builder.profiles[profile_id-1]

    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)})

    else:

        data = {
            'day': day_id,
            'ice': profile.get_ice()
        }

        return JsonResponse(data)
