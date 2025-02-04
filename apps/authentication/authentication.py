import firebase_admin
from firebase_admin import auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token["uid"]
        except Exception as e:
            raise AuthenticationFailed("Invalid Firebase token")

        User = get_user_model()  # Get the custom user model
        user, created = User.objects.get_or_create(username=uid)
        return (user, None)