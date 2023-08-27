from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User
from apps.material.models import Character
from apps.subscription.models import Subscription
from apps.verification.models import VerificationCode


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request: Request):
    try:
        params = request.data
        mobile_phone = params.get('mobile_phone')
        code = params.get('code')
        password = params.get('password')
        if not mobile_phone or not code or not password:
            return Response({'error': '参数缺失'}, status=status.HTTP_400_BAD_REQUEST)
        
        verification_code = VerificationCode.get_latest(mobile_phone=mobile_phone, code=code)
        if not verification_code or not verification_code.is_valid():
            return Response({'error': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)
        verification_code.invalidate()

        new_user = User.objects.create_user(
            username=mobile_phone, 
            mobile_phone=mobile_phone, 
            password=password,
        )

        trial_subscription = Subscription.objects.create(
            user=new_user,
            expiry_datetime=(timezone.now() + relativedelta(days=3)),
        )

        # TODO: decouple the default character creation from register endpoint
        default_character_a = Character(
            user=new_user, 
            name='小博',
            gender='M',
            role='KNOWLEDGE',
            topic='商业与创业',
            birth_date=date.fromisoformat('1988-01-23'),
            education='DOCTOR',
            hobby='博览群书',
            advantage='熟悉公司创业、经营、管理、人力、财务等领域具有多年经验和知识',
            speaking_style='严谨，擅长冷幽默',
            audience_type='20-35岁的创业者',
            personal_statement='商业首席观察官，有任何有关创业投资、企业经营管理的问题，都可以提问'
        )

        default_character_b = Character(
            user=new_user, 
            name='小朵',
            gender='F',
            role='SALE',
            topic='AIGC课程',
            birth_date=date.fromisoformat('1988-01-23'),
            education='DOCTOR',
            advantage='熟悉AI人工智能技术，AIGC，分享AI实用技巧',
            audience_type='职场打工人、创作者',
            personal_statement='AI课程导师，希望能够成为大家学习的助手和伙伴，让每个人都能轻松学习和应用人工智能，并从中受益'
        )

        Character.objects.bulk_create([default_character_a, default_character_b])
        
        return Response({'id': new_user.id})
    except (ValidationError, ValueError) as e:
        return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)

# def register(request: Request):
#     try:
#         new_user_dict = request.data
#         mobile_phone = new_user_dict.get('mobile_phone')
#         password = new_user_dict.get('password')
#         new_user = User.objects.create_user(
#             username=mobile_phone, 
#             mobile_phone=mobile_phone, 
#             password=password,
#         )

#         # trial_subscription = Subscription.objects.create(
#         #     user=new_user,
#         #     expiry_datetime=(timezone.now() + relativedelta(days=3))
#         # )

#         # TODO: decouple the default character creation from register endpoint
#         default_character_a = Character(
#             user=new_user, 
#             name='小博',
#             gender='M',
#             role='KNOWLEDGE',
#             topic='商业与创业',
#             birth_date=date.fromisoformat('1988-01-23'),
#             education='DOCTOR',
#             hobby='博览群书',
#             advantage='熟悉公司创业、经营、管理、人力、财务等领域具有多年经验和知识',
#             speaking_style='严谨，擅长冷幽默',
#             audience_type='20-35岁的创业者',
#             personal_statement='商业首席观察官，有任何有关创业投资、企业经营管理的问题，都可以提问'
#         )

#         default_character_b = Character(
#             user=new_user, 
#             name='小朵',
#             gender='F',
#             role='SALE',
#             topic='AIGC课程',
#             birth_date=date.fromisoformat('1988-01-23'),
#             education='DOCTOR',
#             advantage='熟悉AI人工智能技术，AIGC，分享AI实用技巧',
#             audience_type='职场打工人、创作者',
#             personal_statement='AI课程导师，希望能够成为大家学习的助手和伙伴，让每个人都能轻松学习和应用人工智能，并从中受益'
#         )

#         Character.objects.bulk_create([default_character_a, default_character_b])
        
#         return Response({'id': new_user.id})
#     except (ValidationError, ValueError) as e:
#         return Response({'error': '输入参数无效'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_info(request: Request):
    return Response({
        'id': request.user.id,
        'mobile_phone': request.user.mobile_phone,
    })


@api_view(['POST'])
def log_out(request: Request):
    if request.auth:
        # request.auth is a rest_framework.authtoken.models.Token object
        request.auth.delete()
    
    return Response()