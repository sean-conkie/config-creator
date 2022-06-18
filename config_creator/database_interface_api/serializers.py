from .models import *
from rest_framework import serializers


class ConnectionSerializer(serializers.Serializer):
    class Meta:
        model = Connection
        fields = ["id", "name", "connectionstring", "connectiontype"]
