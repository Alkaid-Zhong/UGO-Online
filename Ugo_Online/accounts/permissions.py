from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    """
    仅允许角色为 'SELLER' 的用户访问
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False  # 让 IsAuthenticated 处理未认证的情况
        if user.role != 'SELLER':
            raise PermissionDenied(detail='用户不是卖家')
        return True
