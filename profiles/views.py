# encoding: utf-8
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.http import JsonResponse
from django.apps import apps


@api_view(http_method_names=["GET"])
def home(request):

    html = """<html>
    
    <head>
        <title>Profiles</title>
    </head>
    
    <body>
        <h1>Profiles</h1>
        <p>Author: Branimir Georgiev</p>
        
        <p>
            This is a simple API that allows you to manage profiles and
            calculate costs for each profile.
        </p>
        
        <p>Endpoints:</p>
        
        <ul>
            <li>GET /profiles/overview/</li>
            <li>GET /profiles/overview/{day_id}/</li>
            <li>GET /profiles/{profile_id}/overview/{day_id}/</li>
            <li>GET /profiles/{profile_id}/days/{day_id}/</li>
            <li>GET /profiles/logs/</li>
            <li>GET /profiles/config/</li>
        </ul>
    """

    return HttpResponse(html)


@api_view(http_method_names=["GET"])
def index(request):
    return HttpResponse("You're at the polls index.")


@api_view(http_method_names=["GET"])
def get_overall_overview(request):

    # Get the app
    app = apps.get_app_config("profiles")

    # Get the number of teams
    num_teams = app.config.num_teams

    try:
        # Build a wall with the given number of teams and days
        app.manager.build(num_teams=num_teams, days=30)

    # Something went wrong
    except Exception as e:
        return HttpResponse(status=500, content=str(e))

    # Everything went well
    else:

        # Prepare the data
        data = {
            'day': None,
            'cost': app.manager.get_cost()
        }

        # Return the data
        return JsonResponse(data)


@api_view(http_method_names=["GET"])
def get_day_overview(request, day_id):

    # Get the app
    app = apps.get_app_config("profiles")

    # Get the number of teams
    num_teams = app.config.num_teams

    try:
        # Build a wall with the given number of teams and days
        app.manager.build(num_teams=num_teams, days=day_id)

    # Something went wrong
    except Exception as e:
        return HttpResponse(status=500, content=str(e))

    # Everything went well
    else:

        # Prepare the data
        data = {
            'day': day_id,
            'cost': app.manager.get_cost()
        }

        # Return the data
        return JsonResponse(data)


@api_view(http_method_names=["GET"])
def get_profile_overview(request, profile_id, day_id):

    # Get the app
    app = apps.get_app_config("profiles")

    # Get the number of teams
    num_teams = app.config.num_teams

    try:
        # Build a wall with the given number of teams and days
        app.manager.build(num_teams=num_teams, days=day_id)

        # Get the profile with the given ID
        profile = app.manager.get_profile(profile_id - 1)

    # Something went wrong
    except Exception as e:
        return HttpResponse(status=500, content=str(e))

    # Everything went well
    else:

        # Prepare the data
        data = {
            'day': day_id,
            'cost': profile.get_cost()
        }

        # Return the data
        return JsonResponse(data)


@api_view(http_method_names=["GET"])
def get_day_data(request, profile_id, day_id):

    # Get the app
    app = apps.get_app_config("profiles")

    # Get the number of teams
    num_teams = app.config.num_teams

    try:
        # Build a wall with the given number of teams and days
        app.manager.build(num_teams=num_teams, days=day_id)

        # Get the profile with the given ID
        profile = app.manager.get_profile(profile_id - 1)

    # Something went wrong
    except Exception as e:
        return HttpResponse(status=500, content=str(e))

    # Everything went well
    else:

        # Prepare the data
        data = {
            'day': day_id,
            'ice': profile.get_ice()
        }

        # Return the data
        return JsonResponse(data)


def get_logs(request):

    # Get the app
    app = apps.get_app_config("profiles")

    try:
        # Get the logs from the manager
        logs = app.manager.get_logs()

    # Something went wrong
    except Exception as e:
        return HttpResponse(status=500, content=str(e))

    # Everything went well
    else:
        # Return the logs
        return JsonResponse(logs)


@api_view(http_method_names=["POST", "GET"])
def handle_config(request):

    # Get the app
    app = apps.get_app_config("profiles")

    # GET request
    if request.method == "GET":

        try:
            # Get the configuration data
            data = app.config.get_params()

        # Something went wrong
        except Exception as e:
            return HttpResponse(status=500, content=str(e))

        # Everything went well
        else:
            return JsonResponse(data)

    # POST request
    elif request.method == "POST":

        try:
            # Set the new configuration data
            app.config.set_params(request.data)

            # Get the new configuration data
            data = {"status": "success"}

        # Something went wrong
        except Exception as e:
            return HttpResponse(status=400, content=str(e))

        # Everything went well
        else:
            return JsonResponse(data)
