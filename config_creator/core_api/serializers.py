from core.models import Field
from rest_framework import serializers


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = [
            "name",
            "source_column",
            "source_name",
            "transformation",
            "is_primary_key",
        ]
