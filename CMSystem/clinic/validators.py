from django.contrib.auth import get_user_model
from datetime import date
from django.core.exceptions import ValidationError
import re

# Validate if a username exists in the user model
def validate_username_exists(username):
    User = get_user_model()  # Dynamically fetch the user model
    if not User.objects.filter(username=username).exists():
        raise ValidationError("The username does not exist.")

# Validate mobile number format
def validate_mobile_number(value):
    if not value.isdigit():
        raise ValidationError("Mobile number should contain only digits.")
    if len(value) != 10:
        raise ValidationError("Mobile number must be exactly 10 digits.")

# (Optional) Uncomment and use the following if email validation is required
# def validate_email(email):
#     """Ensure the email is valid."""
#     email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#     if not re.match(email_regex, email):
#         raise ValidationError("Enter a valid email address.")

# Validate date of birth (DOB) is not in the future
def validate_dob(value):
    if value > date.today():
        raise ValidationError("Date of birth cannot be in the future.")

# Validate joining date is not in the future
def validate_joining_date(value):
    if value > date.today():
        raise ValidationError("Joining date cannot be in the future.")
