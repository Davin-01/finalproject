from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

class CookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None  # No token found in cookies

        try:
            validated_token = AccessToken(access_token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        return validated_token.user, None  # Return user and None for auth info



