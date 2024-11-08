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


def list_response(paginated_response, paginator):

    return api_response(
        True,
        code=0,
        message="查询返回成功",
        data={
            "count": paginated_response["count"],
            "next": paginated_response["next"],
            "previous": paginated_response["previous"],
            "shops": paginated_response["results"],
            "total_count": paginator.page.paginator.count,
            "total_page": paginator.page.paginator.num_pages,
            "cur_page": paginator.page.number
        }
    )
