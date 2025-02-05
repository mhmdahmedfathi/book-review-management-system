from rest_framework import authentication
from .exceptions import InvalidAuthToken
from user.models import User
from rest_framework.authtoken.models import Token

class MiddlewareAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise InvalidAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = Token.objects.get(key=id_token)
        except Token.DoesNotExist:
            raise InvalidAuthToken("Invalid auth token provided")
        
        user = User.objects.get(id=decoded_token.user_id)
        return user, None
