from rest_framework import serializers
from api_keys_server.models import APIKey


class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ('__all__')

