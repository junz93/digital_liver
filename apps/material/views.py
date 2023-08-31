from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Character, QuestionAnswerLibrary, QuestionAnswer, SpeechLibrary, Speech, WordsLibrary, Words
from .serializers import CharacterSerializer, QuestionAnswerLibrarySerializer, QuestionAnswerSerializer, SpeechLibrarySerializer, SpeechSerializer, WordsLibrarySerializer, WordsSerializer


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


@api_view(['POST'])
def create_question_library(request: Request):
    library_serializer = QuestionAnswerLibrarySerializer(data=request.data)
    if not library_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    library = library_serializer.save(user=request.user)
    return Response({'id': library.id})

@api_view(['GET'])
def get_all_question_libraries(request: Request):
    libraries = QuestionAnswerLibrary.objects.filter(user_id=request.user.id)
    library_serializer = QuestionAnswerLibrarySerializer(libraries, many=True)
    return Response(library_serializer.data)

@api_view(['POST'])
def create_question(request: Request):
    question_serializer = QuestionAnswerSerializer(data=request.data)
    if not question_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    question = question_serializer.save()
    return Response({'id': question.id})

@api_view(['POST'])
def delete_question(request: Request, id: int):
    QuestionAnswer.objects.filter(id=id).delete()
    return Response()

@api_view(['GET'])
def get_question(request: Request, id: int):
    try:
        question = QuestionAnswer.objects.get(id=id)
    except QuestionAnswer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    question_serializer = QuestionAnswerSerializer(question)
    return Response(question_serializer.data)

@api_view(['POST'])
def update_question(request: Request, id: int):
    try:
        question = QuestionAnswer.objects.get(id=id)
    except QuestionAnswer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    question_serializer = QuestionAnswerSerializer(question, data=request.data)
    if not question_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    question_serializer.save()
    return Response()

@api_view(['GET'])
def get_all_questions_in_library(request: Request, library_id: int):
    questions = QuestionAnswer.objects.filter(library_id=library_id)
    question_serializer = QuestionAnswerSerializer(questions, many=True)
    return Response(question_serializer.data)

@api_view(['POST'])
def create_speech_library(request: Request):
    library_serializer = SpeechLibrarySerializer(data=request.data)
    if not library_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    library = library_serializer.save(user=request.user)
    return Response({'id': library.id})

@api_view(['GET'])
def get_all_speech_libraries(request: Request):
    libraries = SpeechLibrary.objects.filter(user_id=request.user.id)
    library_serializer = SpeechLibrarySerializer(libraries, many=True)
    return Response(library_serializer.data)

@api_view(['POST'])
def create_speech(request: Request):
    speech_serializer = SpeechSerializer(data=request.data)
    if not speech_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    speech = speech_serializer.save()
    return Response({'id': speech.id})

@api_view(['POST'])
def delete_speech(request: Request, id: int):
    Speech.objects.filter(id=id).delete()
    return Response()

@api_view(['GET'])
def get_speech(request: Request, id: int):
    try:
        speech = Speech.objects.get(id=id)
    except Speech.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    speech_serializer = SpeechSerializer(speech)
    return Response(speech_serializer.data)

@api_view(['GET'])
def get_all_speeches_in_library(request: Request, library_id: int):
    speeches = Speech.objects.filter(library_id=library_id)
    speech_serializer = SpeechSerializer(speeches, many=True)
    return Response(speech_serializer.data)

@api_view(['POST'])
def update_speech(request: Request, id: int):
    try:
        speech = Speech.objects.get(id=id)
    except Speech.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    speech_serializer = SpeechSerializer(speech, data=request.data)
    if not speech_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    speech_serializer.save()
    return Response()
        

@api_view(['POST'])
def create_words_library(request: Request):
    library_serializer = WordsLibrarySerializer(data=request.data)
    if not library_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    library = library_serializer.save(user=request.user)
    return Response({'id': library.id})

@api_view(['GET'])
def get_all_words_libraries_by_type(request: Request, library_type: str):
    libraries = WordsLibrary.objects.filter(user_id=request.user.id, library_type=library_type)
    library_serializer = WordsLibrarySerializer(libraries, many=True)
    return Response(library_serializer.data)

@api_view(['POST'])
def create_word(request: Request):
    word_serializer = WordsSerializer(data=request.data)
    if not word_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    word = word_serializer.save()
    return Response({'id': word.id})

@api_view(['POST'])
def delete_word(request: Request, id: int):
    Words.objects.filter(id=id).delete()
    return Response()

@api_view(['GET'])
def get_word(request: Request, id: int):
    try:
        word = Words.objects.get(id=id)
    except Words.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    word_serializer = WordsSerializer(word)
    return Response(word_serializer.data)

@api_view(['POST'])
def update_word(request: Request, id: int):
    try:
        word = Words.objects.get(id=id)
    except Words.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    word_serializer = WordsSerializer(word, data=request.data)
    if not word_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    word_serializer.save()
    return Response()

@api_view(['GET'])
def get_all_words_in_library(request: Request, library_id: int):
    words = Words.objects.filter(library_id=library_id)
    word_serializer = WordsSerializer(words, many=True)
    return Response(word_serializer.data)


