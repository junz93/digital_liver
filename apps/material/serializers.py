from rest_framework import serializers

from .models import Character


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        exclude = [
            'user',
            'created_datetime',
            'updated_datetime',
        ]
