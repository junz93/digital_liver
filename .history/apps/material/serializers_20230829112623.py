from rest_framework import serializers

from .models import Character, QuestionAnswerLibrary, QuestionAnswer, SpeechLibrary, Speech


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        exclude = [
            'user',
            'created_datetime',
            'updated_datetime',
        ]

class QuestionAnswerLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswerLibrary
        exclude = [
            'user',
            'created_datetime',
            'updated_datetime',
        ]

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        exclude = [
            'library',
            'created_datetime',
            'updated_datetime',
        ]

class SpeechLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeechLibrary
        exclude = [
            'user',
            'created_datetime',
            'updated_datetime',
        ]

class SpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speech
        exclude = [
            'library',
            'created_datetime',
            'updated_datetime',
        ]
