from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            MinLengthValidator(3, 'Email must be at least 3 character.'),
            MaxLengthValidator(254, 'Email cannot be more than 254 characters.'),
        ]
    )
    username = serializers.CharField(
        required=True, 
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9\_\.]+$',
                message="The username can only contain letters, numbers, or the following special characters: '_' or '.'"
            ),
            MinLengthValidator(1, 'Username must be at least 1 character.'),
            MaxLengthValidator(20, 'Username cannot be more than 20 characters.'),
        ]
    )
    password = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(8, 'The password must be at least 8 characters.')
        ],
        write_only=True,
    )

    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'username', 'password')