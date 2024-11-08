# ecommerce/exceptions.py

from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from .utils import api_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, NotAuthenticated):
            return api_response(False, code=401, message='用户未登录', data=response.data)
        elif isinstance(exc, PermissionDenied):
            detail = exc.detail if hasattr(exc, 'detail') else '用户没有权限'
            return api_response(False, code=403, message=detail, data=response.data)
        else:
            return api_response(False, code=400, message=response.data.get('detail', '发生错误'), data=response.data)
    else:
        error_detail = str(exc) if exc else '未知错误'
        return api_response(False, code=500, message='服务器内部错误', data={'error': error_detail})
