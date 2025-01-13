import random
import string
from apps.authentication.models import UserProfile

def generate_unique_username(base_username):
    """Generate a unique username by appending a random string."""
    if not base_username:  # Check if base_username is valid
        return "default_username"  # Fallback if base_username is empty or invalid
    
    while True:
        # Append a random 4-character alphanumeric suffix to the base username
        unique_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        unique_username = f"{base_username}_{unique_suffix}"

        # Check if this username already exists
        if not UserProfile.objects.filter(username=unique_username).exists():
            return unique_username
        
        # If the username exists, try again by generating a new suffix
        print(f"Username {unique_username} already exists. Retrying...")



def get_bearer_token(header):
    if not header:
        return None
    return header.split(' ')[1] if header.startswith('Bearer ') else header
