from rest_framework import permissions

class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.tipoUser == "participante"


class IsExpert(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.tipoUser == "evaluador"


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.tipoUser == "admin"
