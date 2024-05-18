from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        print(f"User: {request.user}")  # Verificar el usuario
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"User is superuser: {request.user.is_superuser}")
        print(f"Authorization header: {request.headers.get('Authorization')}")
        return request.user and request.user.is_authenticated and request.user.is_superuser