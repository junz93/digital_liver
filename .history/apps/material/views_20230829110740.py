from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Character
from .serializers import CharacterSerializer


@api_view(['POST'])
def create_character(request: Request):
    character_serializer = CharacterSerializer(data=request.data)
    if not character_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)

    character = character_serializer.save(user=request.user)
    return Response({'id': character.id})


@api_view(['POST'])
def update_character(request: Request, id: int):
    try:
        character = Character.objects.get(id=id, user_id=request.user.id)
    except Character.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    character_serializer = CharacterSerializer(character, data=request.data)
    if not character_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)

    character_serializer.save()
    return Response()


@api_view(['POST'])
def delete_character(request: Request, id: int):
    Character.objects.filter(id=id, user_id=request.user.id).delete()
    return Response()


@api_view(['GET'])
def get_character(request: Request, id: int):
    try:
        character = Character.objects.get(id=id, user_id=request.user.id)
    except Character.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    character_serializer = CharacterSerializer(character)
    return Response(character_serializer.data)


@api_view(['GET'])
def get_all_characters(request: Request):
    characters = Character.objects.filter(user_id=request.user.id)
    character_serializer = CharacterSerializer(characters, many=True)
    return Response(character_serializer.data)

