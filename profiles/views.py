# encoding: utf-8
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.http import JsonResponse
from django.apps import apps


@api_view(http_method_names=["GET"])
def home(request):
    return HttpResponse("Hello, world!")


@api_view(http_method_names=["GET"])
def index(request):
    return HttpResponse("You're at the polls index.")


@api_view(http_method_names=["GET"])
def get_overall_overview(request):

    app = apps.get_app_config("profiles")
    num_teams = app.config.num_teams

    try:
        app.manager.build(num_teams=num_teams, days=30)

    except Exception as e:
        return JsonResponse({'error': str(e)})

    else:

        data = {
            'day': None,
            'cost': app.manager.get_cost()
        }

        return JsonResponse(data)


@api_view(http_method_names=["GET"])
def get_day_overview(request, day_id):

    app = apps.get_app_config("profiles")
    num_teams = app.config.num_teams

    try:
        app.manager.build(num_teams=num_teams, days=day_id)

    except Exception as e:
        return JsonResponse({'error': str(e)})

    else:
        data = {
            'day': day_id,
            'cost': app.manager.get_cost()
        }

        return JsonResponse(data)


@api_view(http_method_names=["GET"])
def get_profile_overview(request, profile_id, day_id):

    app = apps.get_app_config("profiles")
    num_teams = app.config.num_teams

    try:
        app.manager.build(num_teams=num_teams, days=day_id)
        profile = app.manager.get_profile(profile_id - 1)

    except Exception as e:
        return JsonResponse({'error': str(e)})

    else:
        data = {
            'day': day_id,
            'cost': profile.get_cost()
        }

        return JsonResponse(data)


@api_view(http_method_names=["GET"])
def get_day_data(request, profile_id, day_id):
    app = apps.get_app_config("profiles")
    num_teams = app.config.num_teams

    try:
        app.manager.build(num_teams=num_teams, days=day_id)
        profile = app.manager.get_profile(profile_id - 1)

    except Exception as e:
        return JsonResponse({'error': str(e)})

    else:

        data = {
            'day': day_id,
            'ice': profile.get_ice()
        }

        return JsonResponse(data)


@api_view(http_method_names=["POST", "GET"])
def handle_config(request):

    # Get the app
    app = apps.get_app_config("profiles")

    try:
        if request.method == "GET":
            return JsonResponse(app.config.get_params())

        else:
            # Set the parameters
            app.config.set_params(request.data)

            # Return the response
            return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'error': str(e)})
