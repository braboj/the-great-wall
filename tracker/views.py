from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse


def home(request):
    return HttpResponse('Hello, World!')


def total_cost(request):
    data = {
        'day': None,
        'total_cost': 0
    }

    return JsonResponse(data)


def total_daily_cost(request, day):
    data = {
        'day': day,
        'total_cost': 0
    }

    return JsonResponse(data)


def total_daily_profile_cost(request, profile, day):
    data = {
        'profile': profile,
        'day': day,
        'total_cost': 0
    }

    return JsonResponse(data)


def profile_day_detail(request, profile, day):
    # Prepare the data to be returned in the response
    data = {
        'profile': profile,
        'day': day,
        'details': ''
    }

    return JsonResponse(data)
