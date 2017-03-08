# coding=utf-8
from io import BytesIO

import json
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import util
from api_keys_server.models import APIKey
from serializers import APIKeySerializer


class APIKeyList(APIView):
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    @permission_classes((permissions.AllowAny,))
    def get(self, request, format=None):
        api_keys_ = APIKey.objects.all()
        serializer = APIKeySerializer(api_keys_, many=True)
        context = {'api_keys': serializer.data}
        return Response(context, status=200, template_name='api_keys.html')

    @permission_classes(permissions.IsAuthenticated,)
    def post(self, request, format=None):
        serializer = APIKeySerializer(data=request.data)
        context = {}

        if serializer.is_valid():
            try:
                serializer.save()
                context['message'] = 'API Key generada'
                status = 201
            except StandardError:
                context['message'] = serializer['mail'].errors[0]
                status = 200
        else:
            status = 200
            context['message'] = serializer['mail'].errors[0]
        api_keys_ = APIKey.objects.all()
        context['api_keys'] = api_keys_
        return Response(context, status=status, content_type='text/html', template_name='api_keys.html')


class WordsDuplicatedDetail(APIView):
    @permission_classes((permissions.AllowAny,))
    def get(self, request):
        return find_duplicates(request)


def index(request):
    return render(request, 'index.html', {})


def api_view(request):
    context = {}
    return render(request, 'api.html', context)


def find_duplicates(request):
    try:
        api_key = request.META['HTTP_API_KEY']
        if not util.valid_key(api_key):
            return Response(u'API Key inválida',status=401, content_type="application/json")
        else:
            apiKey = APIKey.objects.filter(api_key=api_key).get()
            apiKey.requests += 1
            apiKey.save()
    except KeyError:
        return Response(u'API Key inválida',status=401, content_type="application/json")
    try:
        data = request.META['HTTP_DATA']
        stream = BytesIO(data)
        data_list = JSONParser().parse(stream)
        duplicates = util.get_duplicates(data_list)
    except (KeyError, ParseError):
        return Response(u'El formato de los datos no es válido', status=400, content_type="application/json")

    response = json.dumps(duplicates)
    return Response({'duplicates': response}, status=200, content_type="application/json")
