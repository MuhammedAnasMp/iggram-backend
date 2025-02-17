import json
from celery import shared_task
from datetime import datetime

from django.http import JsonResponse
from .models import ReelUploadTask
from instagrapi import Client  # or your choice of library
from rest_framework.views import APIView
from apps.authentication.authentication import FirebaseAuthentication
from instagrapi.exceptions import UnknownError, PleaseWaitFewMinutes, BadCredentials, ChallengeRequired
from instagrapi import Client
cl=Client()
@shared_task
def upload_reel_task(reel_upload_id):
    reel_upload = ReelUploadTask.objects.get(id=reel_upload_id)
    
    # Logic for uploading the reel (using Instagrapi or your method)
    client = Client()
    client.login(reel_upload.account.username, reel_upload.account.password)  # Use proper login

    # Handle uploading video from URL
    video_url = reel_upload.video_url
    # Add logic to fetch and upload video from URL, including caption, language, etc.

    # Update task status
    reel_upload.status = 'uploaded'
    reel_upload.save()




from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import json
from instagrapi import Client
from instagrapi.exceptions import (
    UnknownError, PleaseWaitFewMinutes, BadCredentials, ChallengeRequired
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import InstagramAccount, UserProfile
from .serializer import InstagramAccountSerializer
from rest_framework.generics import ListAPIView
class UserInstagramAccountsView(ListAPIView):
    serializer_class = InstagramAccountSerializer
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self):
        return InstagramAccount.objects.filter(user=self.request.user)
class IgLoginClassView(APIView):
 

    authentication_classes = [FirebaseAuthentication]
    def post(self, request):
        try:
            body = json.loads(request.body.decode('utf-8'))  # Safely parse JSON
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        username = body.get('username')
        password = body.get('password')

        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)

        # Get the authenticated user
        user = request.user
        print(user.username)
        if not isinstance(user, UserProfile):
            return JsonResponse({"error": "User authentication failed"}, status=401)

        cl = Client()

        try:
            cl.login(username, password)
            user_info = cl.account_info()
            session_data = cl.get_settings()  # Get session data (Instagrapi's load.json content)

            # Extract user info
            instagram_account, created = InstagramAccount.objects.update_or_create(
                user=user,
                username=user_info.username,
                defaults={
                    "full_name": user_info.full_name,
                    "profile_pic_url": str(user_info.profile_pic_url),
                    "is_verified": user_info.is_verified,
                    "biography": user_info.biography,
                    "external_url": user_info.external_url,
                    "email": user_info.email,
                    "phone_number": user_info.phone_number,
                    "gender": user_info.gender,
                    "is_business": user_info.is_business,
                    "birthday": user_info.birthday,
                    "auth_data": session_data,
                }
            )

            return JsonResponse({
                "message": "Login successful",
                "username": user_info.username,
                "full_name": user_info.full_name,
                "profile_pic_url": str(user_info.profile_pic_url),
                "account_status": "Created" if created else "Updated"
            }, status=200)

        except BadCredentials:
            return JsonResponse({"error": "Invalid username or password"}, status=401)
        except PleaseWaitFewMinutes:
            return JsonResponse({"error": "Please wait a few minutes before trying again"}, status=429)
        except ChallengeRequired:
            return JsonResponse({"error": "Verification required. Check Instagram for verification."}, status=403)
        except UnknownError:
            return JsonResponse({"error": "We can't find an account with admin"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)