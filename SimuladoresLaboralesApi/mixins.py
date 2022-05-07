import jwt
from rest_framework import permissions, status
from rest_framework.exceptions import APIException
from unityREST import settings


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return True


class IsExpert(permissions.BasePermission):

    def has_permission(self, request, view):
        return True


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return True


class ValidateToken(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            payload = jwt.decode(token, settings.TOKEN_KEY, algorithms=['HS256'])
            user = payload
            if payload["tipoUser"] == "participante":
                pass
            elif payload["tipoUser"] == "evaluador":
                pass
            elif payload["tipoUser"] == "admin":
                pass
            request.user = user
            return True
        except Exception as e:
            print(e)
            raise GenericAPIException(detail="token invalid")
            # return False


class GenericAPIException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'UNAUTHORIZED'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code
