from django.http import HttpResponse ,JsonResponse
from django.contrib.auth import authenticate, login ,logout
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from apps.authentication.models import UserProfile
from apps.authentication.utility import generate_unique_username,get_bearer_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated ,AllowAny
from firebase_admin import auth
from cloudinary.uploader import upload
import logging
from django.middleware.csrf import get_token
logger = logging.getLogger(__name__)



def index(request):
    return HttpResponse("Hello, world! Welcome to the Blog app.")


        
def session_check_view(request):
    if request.user.is_authenticated:
        # Return the username, email, and authenticated status
        return JsonResponse({
            "authenticated": True,
            "user": {
                "username": request.user.username,
                "email": request.user.email,
                "uid": request.user.firebase_uid,
                "profile_image": request.user.photo
                
            }
        })
    return JsonResponse({"authenticated": False})

@ensure_csrf_cookie  # Ensures that a CSRF cookie is set
def csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})




@csrf_exempt
def verifytoken(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid method'}, status=405)

    token = get_bearer_token(request.headers.get('Authorization'))
    if not token:
        return JsonResponse({'error': 'Please provide the token'}, status=400)

    try:
        # Verify Firebase token
        decoded_token = auth.verify_id_token(token)
        firebase_uid = decoded_token['uid']

        # Check if the user exists or create a new one
        user, created = UserProfile.objects.get_or_create(firebase_uid=firebase_uid)
        if created:
            user.first_name = decoded_token.get('name', '')
            user.email = decoded_token.get('email', '')
            photo_url = decoded_token.get('picture', '')

            if photo_url:
            # Upload the photo to Cloudinary
                try:
                    upload_result = upload(photo_url, folder="user_photos/")
                    user.photo = upload_result.get('secure_url')  # Save the Cloudinary URL directly
                except Exception as e:
                    return JsonResponse({'error': f"Error uploading photo: {str(e)}"}, status=500)
            user.phone_number = decoded_token.get('phone_number', '')
            user.provider = decoded_token.get('firebase', {}).get('sign_in_provider', '')

            # Generate a unique username
            base_username = (
                user.first_name.lower().replace(' ', '') or
                decoded_token.get('name', '').lower().replace(' ', '') or
                (user.email.split('@')[0].lower() if user.email else '')
            )
            user.username = (
                base_username
                if not UserProfile.objects.filter(username=base_username).exists()
                else generate_unique_username(base_username)
            )

            user.save()

        # Log the user in and create a session
        login(request, user)
        return JsonResponse({
            'username': request.user.username,
            'email': request.user.email,
            'uid': user.firebase_uid,
            'profile_image': user.photo, 
            'message': 'Login successful'
        }, status=200)

    except auth.ExpiredIdTokenError:
        return JsonResponse({'error': 'Token has expired'}, status=400)
    except auth.RevokedIdTokenError:
        return JsonResponse({'error': 'Token has been revoked'}, status=400)
    except auth.InvalidIdTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    except Exception as e:
        logger.error("Unexpected error during token verification: %s", str(e))
        return JsonResponse({'error': 'An error occurred'}, status=500)


class PublicView(APIView):
    permission_classes = [IsAuthenticated]  # Override IsAuthenticated

    def get(self, request, *args, **kwargs):
        return Response({"message": "This endpoint is public!"})
    
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'}, status=200)
    
def post_test(request):
    print("sample post")

    return JsonResponse({'message': 'Sample post'}, status=200)
