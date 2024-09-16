from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from accounts.models import APIToken


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AuthenticationFailed('Authorization header is missing')

        if 'Bearer' not in auth_header:
            raise AuthenticationFailed('No token provided')

        try:
            token_string = auth_header.split(' ')[-1]
            api_token = APIToken.objects.get(token=token_string)

            if not api_token.verify_token():
                raise AuthenticationFailed('Token expired')
            return api_token.user, api_token
        except APIToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
