"""
If you delete the user model, the corresponding Firebase authentication data may become redundant. In such cases, run the following command to delete all Firebase users as well:

# python manage.py delete_firebase_users

"""
import os
import firebase_admin
from firebase_admin import credentials, auth
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Delete all users from Firebase Authentication'

    def handle(self, *args, **kwargs):
        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate({
                "type": os.environ.get('FIREBASE_TYPE'),
                "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
                "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
                "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace("\\n", "\n"),
                "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
                "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
                "auth_uri": os.environ.get('FIREBASE_AUTH_URI'),
                "token_uri": os.environ.get('FIREBASE_TOKEN_URI'),
                "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
                "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_X509_CERT_URL')
            })
            firebase_admin.initialize_app(cred)

        def get_all_user_ids():
            user_ids = []
            page = auth.list_users()
            while page:
                for user in page.users:
                    user_ids.append(user.uid)
                page = page.get_next_page()
            return user_ids

        def bulk_delete_users(user_ids):
            while user_ids:
                batch = user_ids[:1000] 
                user_ids = user_ids[1000:]
                try:
                    result = auth.delete_users(batch)
                    self.stdout.write(self.style.SUCCESS(f'Successfully deleted {result.success_count} users'))
                    if result.failure_count:
                        self.stdout.write(self.style.ERROR(f'Failed to delete {result.failure_count} users:'))
                        for err in result.errors:
                            self.stdout.write(self.style.ERROR(f'Error: {err.reason}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error deleting users: {e}'))

        user_ids = get_all_user_ids()
        self.stdout.write(self.style.SUCCESS(f'Total users to delete: {len(user_ids)}'))
        bulk_delete_users(user_ids)
        self.stdout.write(self.style.SUCCESS('Completed deleting all users from Firebase Authentication.'))
