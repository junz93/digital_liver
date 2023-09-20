from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import FileResponse
import os
from django.conf import settings
from .models import Character, QuestionAnswerLibrary, QuestionAnswer, SpeechLibrary, Speech, WordsLibrary, Words, Lens, Image, UserImage, Environment, UserEnvironment, EnvironmentOrder, ImageOrder, LiveConfig
from .serializers import CharacterSerializer, QuestionAnswerLibrarySerializer, QuestionAnswerSerializer, \
    SpeechLibrarySerializer, SpeechSerializer, WordsLibrarySerializer, WordsSerializer, LensSerializer, ImageSerializer, UserImageSerializer, EnvironmentSerializer, UserEnvironmentSerializer, LiveConfigSerializer
from services import payment


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

#镜头
@api_view(['GET'])
def get_all_lenses(request: Request):
    lenses = Lens.objects.filter(user=request.user.id)
    lens_serializer = LensSerializer(lenses, many=True)
    return Response(lens_serializer.data)

@api_view(['GET'])
def get_lens(request: Request, id: int):
    try:
        lens = Lens.objects.get(id=id, user=request.user.id)
    except Lens.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    lens_serializer = LensSerializer(lens)
    return Response(lens_serializer.data)

@api_view(['POST'])
def create_lens(request: Request):
    lens_serializer = LensSerializer(data=request.data)
    if not lens_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    lens = lens_serializer.save(user=request.user)
    return Response({'id': lens.id})

@api_view(['POST'])
def update_lens(request: Request, id: int):
    try:
        lens = Lens.objects.get(id=id, user=request.user.id)
    except Lens.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    lens_serializer = LensSerializer(lens, data=request.data)
    if not lens_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    lens_serializer.save()
    return Response()

@api_view(['POST'])
def delete_lens(request: Request, id: int):
    Lens.objects.filter(id=id, user=request.user.id).delete()
    return Response()


#形象
@api_view(['GET'])
def get_all_images(request: Request):
    user_images = UserImage.objects.filter(user=request.user.id)
    image_ids = [user_image.image.id for user_image in user_images]
    images = Image.objects.filter(id__in=image_ids)
    image_serializer = ImageSerializer(images, many=True)
    return Response(image_serializer.data)

#测试用创建形象
@api_view(['POST'])
def create_image(request: Request):
    image_serializer = ImageSerializer(data=request.data)
    if not image_serializer.is_valid():
        return Response({'error': '输入参数无效','details': image_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    image = image_serializer.save()
    return Response({'id': image.id})

#测试用模拟购买操作
@api_view(['POST'])
def bind_user_image(request: Request, image_id: int):
    try:
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user_image = UserImage.objects.create(user=request.user, image=image)
    return Response({'id': user_image.id})

@api_view(['POST'])
def update_image(request: Request, image_id: int):
    try:
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    image_serializer = ImageSerializer(image, data=request.data)
    if not image_serializer.is_valid():
        return Response({'error': '输入参数无效','details': image_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    image_serializer.save()
    return Response()

@api_view(['POST'])
def delete_image(request: Request, image_id: int):
    try:
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    image.delete()
    return Response()



#环境
@api_view(['GET'])
def get_all_environments(request: Request):
    user_environments = UserEnvironment.objects.filter(user=request.user.id)
    environment_ids = [user_environment.environment.id for user_environment in user_environments]
    environments = Environment.objects.filter(id__in=environment_ids)
    environment_serializer = EnvironmentSerializer(environments, many=True)
    return Response(environment_serializer.data)

#测试用创建环境
@api_view(['POST'])
def create_environment(request: Request):
    environment_serializer = EnvironmentSerializer(data=request.data)
    if not environment_serializer.is_valid():
        return Response({'error': '输入参数无效','details': environment_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    environment = environment_serializer.save()
    return Response({'id': environment.id})

#测试用模拟购买操作
@api_view(['POST'])
def bind_user_environment(request: Request, environment_id: int):
    try:
        environment = Environment.objects.get(id=environment_id)
    except Environment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user_environment = UserEnvironment.objects.create(user=request.user, environment=environment)
    return Response({'id': user_environment.id})

@api_view(['POST'])
def update_environment(request: Request, environment_id: int):
    try:
        environment = Environment.objects.get(id=environment_id)
    except Environment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    environment_serializer = EnvironmentSerializer(environment, data=request.data)
    if not environment_serializer.is_valid():
        return Response({'error': '输入参数无效','details': environment_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    environment_serializer.save()
    return Response()

@api_view(['POST'])
def delete_environment(request: Request, environment_id: int):
    try:
        environment = Environment.objects.get(id=environment_id)
    except Environment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    environment.delete()
    return Response()


#支付宝
@api_view(['POST'])
def get_alipay_payment_url_image(request: Request, image_id: int):
    try:
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    order_id = payment.generate_order_id(prefix=ImageOrder.ORDER_ID_PREFIX)
    ImageOrder.objects.create(
        order_id=order_id, 
        user=request.user, 
        image=image,
        amount=image.price,
    )

    url = payment.get_desktop_alipay_payment_url(
        order_id=order_id, 
        subject=f'购买形象: {image.image_name}', 
        total_amount=image.price,
    )
    return Response({'url': url})

@api_view(['POST'])
def get_alipay_payment_url_environment(request: Request, environment_id: int):
    try:
        environment = Environment.objects.get(id=environment_id)
    except Environment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    order_id = payment.generate_order_id(prefix=EnvironmentOrder.ORDER_ID_PREFIX)
    EnvironmentOrder.objects.create(
        order_id=order_id, 
        user=request.user, 
        environment=environment,
        amount=environment.price,
    )

    url = payment.get_desktop_alipay_payment_url(
        order_id=order_id, 
        subject=f'购买背景: {environment.env_name}', 
        total_amount=environment.price,
    )
    return Response({'url': url})


#直播配置
@api_view(['GET'])
def get_live_config(request: Request):
    try:
        live_config = LiveConfig.objects.get(user=request.user)
        live_config_serializer = LiveConfigSerializer(live_config)
        return Response(live_config_serializer.data)
    except LiveConfig.DoesNotExist:
        return Response({})

@api_view(['POST'])
def update_live_config(request: Request):
    live_config, created = LiveConfig.objects.get_or_create(user=request.user)
    live_config_serializer = LiveConfigSerializer(live_config, data=request.data)
    if not live_config_serializer.is_valid():
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)
    live_config_serializer.save()
    return Response(live_config_serializer.data)
