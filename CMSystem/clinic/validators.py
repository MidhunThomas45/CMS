from django.contrib.auth import get_user_model

def validate_username_exists(username):
    User = get_user_model()  # Dynamically fetch the user model
    if not User.objects.filter(username=username).exists():
        raise ValueError("The username does not exist.")