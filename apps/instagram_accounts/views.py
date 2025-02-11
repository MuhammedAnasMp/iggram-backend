from celery import shared_task
from datetime import datetime
from .models import ReelUploadTask
from instagrapi import Client  # or your choice of library

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
