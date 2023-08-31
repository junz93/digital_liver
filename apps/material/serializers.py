from rest_framework import serializers

from .models import Character, QuestionAnswerLibrary, QuestionAnswer, SpeechLibrary, Speech, WordsLibrary, Words


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
            'created_datetime',
            'updated_datetime',
        ]

class WordsLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WordsLibrary
        exclude = [
            'user',
            'created_datetime',
            'updated_datetime',
        ]

class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        exclude = [
            'created_datetime',
            'updated_datetime',
        ]

