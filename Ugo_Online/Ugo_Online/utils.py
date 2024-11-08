from rest_framework import status
from rest_framework.response import Response


def api_response(success, code=0, message='', data=None, status_code=status.HTTP_200_OK):
    if not success and status_code == status.HTTP_200_OK:
        status_code = status.HTTP_400_BAD_REQUEST
    return Response({
        'success': success,
        'code': code,
        'message': message,
        'data': data
    }, status=status_code)
