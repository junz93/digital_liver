# from rest_framework import status
from rest_framework.response import Response


def create_error_response(status_code: int, error: str):
    return Response({'detail': error}, status=status_code)
