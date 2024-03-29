from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 읽기 권한 요청이 들어오면 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 요청자(request.user)가 객체(Blog)의 user와 동일한지 확인
        return obj.user == request.user
    
class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # 읽기 권한 요청이 들어오면 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 관리자인 경우에만 쓰기 권한을 허용
        return request.user and request.user.is_staff