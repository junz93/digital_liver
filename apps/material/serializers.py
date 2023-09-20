from rest_framework import serializers

from .models import Character, QuestionAnswerLibrary, QuestionAnswer, SpeechLibrary, Speech, WordsLibrary, Words, Lens, Image, UserImage, Environment, UserEnvironment, LiveConfig


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

class LensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lens
        exclude = [
            'user',
            'created_datetime',
            'updated_datetime',
        ]

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = [
            'created_datetime',
            'updated_datetime',
        ]

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        exclude = [
            'created_datetime',
            'updated_datetime',
        ]

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        exclude = [
            'created_datetime',
            'updated_datetime',
        ]

class UserEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnvironment
        exclude = [
            'created_datetime',
            'updated_datetime',
        ]

class LiveConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveConfig
        exclude = [
            'user',
            'created_datetime',
            'updated_datetime',
        ]
