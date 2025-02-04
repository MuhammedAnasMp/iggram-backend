from django.http import HttpResponse ,JsonResponse
from django.contrib.auth import authenticate, login ,logout
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from apps.authentication.models import UserProfile, UserProvider
from apps.authentication.utility import generate_unique_username,get_bearer_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from firebase_admin import auth
from cloudinary.uploader import upload
import logging
from django.middleware.csrf import get_token
logger = logging.getLogger(__name__)
import os
import subprocess
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
import hmac
import hashlib
from .authentication import FirebaseAuthentication
import json

def index(request):
    return HttpResponse("Hello, world! Welcome to the Blog app.")

def verify_firebase_token(request):
    body = json.loads(request.body.decode('utf-8'))  # Parse JSON manually
    firebase_token = body.get('firebase_token')
    print(firebase_token)
    try:
        decoded_token = auth.verify_id_token(firebase_token)
        uid = decoded_token['uid']
        email = decoded_token['email']

        # Get or create a Django user
        user, created = UserProfile.objects.get_or_create(username=uid, defaults={'email': email})

        # Return a success response
        return JsonResponse({
            'status': 'success',
            'uid': uid,
            'email': email,
            'user_id': user.id,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class ProtectedView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        return Response({'message': 'You are authenticated!', 'user': request.user.username})




















GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
@csrf_exempt
def git_pull(request):
    if request.method == "POST":
        # Step 1: Verify the GitHub webhook secret
        header_signature = request.META.get('HTTP_X_HUB_SIGNATURE_256')
        if header_signature is None:
            logger.warning("Missing X-Hub-Signature-256 header")
            return HttpResponseForbidden("Permission denied")

        # Compute the HMAC signature
        signature = hmac.new(
            GITHUB_WEBHOOK_SECRET.encode(),
            request.body,
            hashlib.sha256
        ).hexdigest()
        expected_signature = f"sha256={signature}"

        # Compare the signatures securely
        if not hmac.compare_digest(header_signature, expected_signature):
            logger.warning("Invalid webhook signature")
            return HttpResponseForbidden("Invalid signature")

        # Step 2: Perform git pull and migrations
        try:
            repo_path = settings.BASE_DIR

            # Pull changes
            pull_output = subprocess.check_output(['git', 'pull'], cwd=repo_path, text=True)
            logger.info(pull_output)

            # Make migrations
            makemigrations_output = subprocess.check_output(
                ['python', 'manage.py', 'makemigrations'], cwd=repo_path, text=True
            )
            logger.info(makemigrations_output)

            # Migrate
            migrate_output = subprocess.check_output(
                ['python', 'manage.py', 'migrate'], cwd=repo_path, text=True
            )
            logger.info(migrate_output)

            return JsonResponse({"status": "success"})
        except subprocess.CalledProcessError as e:
            logger.error(f"Error during update: {e.output}")
            return JsonResponse({"status": "failed", "error": e.output})
    return JsonResponse({"status": "invalid method"})