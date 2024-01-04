from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

# Signup
class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            MinLengthValidator(3, 'Email must be at least 3 character.'),
            MaxLengthValidator(254, 'Email cannot be more than 254 characters.'),
        ],
        error_messages={
            'invalid': 'Email address must be valid.',
            'unique': 'Email already registered.'
        }   
    )
    username = serializers.CharField(
        required=True, 
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z]',
                message="Username must start with a letter."
            ),
            RegexValidator(
                regex=r'^[a-zA-Z0-9_\.\-]*$',
                message="Username must contain only the following special characters: _."
            ),
            MinLengthValidator(1, 'Username must be at least 1 character.'),
            MaxLengthValidator(20, 'Username cannot be more than 20 characters.'),
        ],
        error_messages={
            'unique': 'Username already registered.'
        }  
    )
    password = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(8, 'Password must be at least 8 characters.'),
            RegexValidator(
                regex=r'^(?=.*[a-zA-Z])',
                message="Password must contain at least 1 letter."
            ),
            RegexValidator(
                regex=r'^(?=.*\d)',
                message="Password must contain at least 1 number."
            ),
            RegexValidator(
                regex=r'^(?=.*[!@#$%^&*()\-_=+<>?/\[\]{}|:;"\',.<>`~])',
                message="Password must contain at least 1 special character."
            )
        ],
        write_only=True,
    )

    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'username', 'password')

# Change password
class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(8, 'Password must be at least 8 characters.'),
            RegexValidator(
                regex=r'^(?=.*[a-zA-Z])',
                message="Password must contain at least 1 letter."
            ),
            RegexValidator(
                regex=r'^(?=.*\d)',
                message="Password must contain at least 1 number."
            ),
            RegexValidator(
                regex=r'^(?=.*[!@#$%^&*()\-_=+<>?/\[\]{}|:;"\',.<>`~])',
                message="Password must contain at least 1 special character."
            )
        ],
        write_only=True,
        style={'input_type': 'password'},
    )
    re_new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, data):
        new_password = data.get('new_password')
        re_new_password = data.get('re_new_password')

        # Validar que las contraseñas coincidan
        if new_password != re_new_password:
            raise serializers.ValidationError({'detail': 'Passwords do not match'})

        # Validar las contraseñas según las políticas de Django
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({'detail': e.messages})

        return data