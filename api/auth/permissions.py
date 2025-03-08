from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class ApiAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.META['REMOTE_ADDR'] != '127.0.0.1':
            raise PermissionDenied('Acesso Negado para este IP.')
        return True
