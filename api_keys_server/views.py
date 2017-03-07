from django.http import HttpResponse
from django.shortcuts import render
import api

from api_keys_server.models import APIKey


def index(request):
    return render(request, 'index.html', {})


def api_keys(request):
    api_keys_ = APIKey.objects.all()
    context = {'api_keys': api_keys_}
    return render(request, 'api_keys.html', context)


def api_view(request):
    context = {}
    return render(request, 'api.html', context)


def find_duplicates(request):
    try:
        api_key = request.META['HTTP_API_KEY']
        if not api.valid_key(api_key):
            return HttpResponse('"code":"401",<br>"status":"unauthorized",<br>', status=401)
        else:
            apiKey = APIKey.objects.filter(api_key=api_key).get()
            apiKey.requests += 1
            apiKey.save()
    except KeyError:
        return HttpResponse('Unauthorized', status=401)
    duplicates_formatted = "{}"
    try:
        data = request.META['HTTP_DATA']
        duplicates = api.find_duplicates(data)
        duplicates_formatted = api.format_response(duplicates)
    except KeyError:
        pass
    return HttpResponse('"code":"200",<br>"status":"success",<br>"duplicates":%s' % duplicates_formatted,
                        status=200,content_type="text/json")

