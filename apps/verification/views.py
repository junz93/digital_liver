from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .models import VerificationCode
from services import sms
from utils.verification import generate_verification_code


@api_view(['POST'])
@permission_classes([AllowAny])
def send_verification_sms(request: Request):
    params = request.data
    if 'mobile_phone' not in params:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    mobile_phone = params['mobile_phone']

    latest_verification_code = VerificationCode.get_latest(mobile_phone=mobile_phone)
    if latest_verification_code and (timezone.now() - latest_verification_code.created_datetime).total_seconds() < 60:
        return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    code = generate_verification_code()
    VerificationCode.objects.create(
        mobile_phone=mobile_phone,
        code=code,
    )

    sms.send_verification_sms(code, mobile_phone)
    
    return Response()


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_sms_code(request: Request):
    params = request.query_params

    if 'mobile_phone' not in params or 'code' not in params:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    mobile_phone = params['mobile_phone']
    code = params['code']

    verification_code = VerificationCode.get_latest(mobile_phone=mobile_phone, code=code)
    is_valid = bool(verification_code and verification_code.is_valid())

    return Response({'is_valid': is_valid})
