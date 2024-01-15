# | ---------------------------------------------------------------------- |
# | ---------------------- IMPORTACIONES NECESARIAS ---------------------- |
# | ---------------------------------------------------------------------- |

from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import Album, File

# | ------------------------------------------------------------------ |
# | ---------------------- SERIALIZADOR USUARIO ---------------------- |
# | ------------------------------------------------------------------ |

# Serializador para la creación de usuario
class CustomUserCreateSerializer(UserCreateSerializer):
    # Validación email
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
    # Validación usuario
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
    # Validación contraseña
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

# | --------------------------------------------------------------------- |
# | ---------------------- SERIALIZADOR CONTRASEÑA ---------------------- |
# | --------------------------------------------------------------------- |
        
# Serializador para comprobar contraseñas válidas de reseteo
class PasswordResetSerializer(serializers.Serializer):
    # Validación nueva contraseña
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
    # Validación contraseña confirmación
    re_new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
    )

    # Validación de ambas contraseñas para efectuar la operación
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
    
# | ----------------------------------------------------------------- |
# | ---------------------- SERIALIZADOR FICHEROS ---------------------- |
# | ----------------------------------------------------------------- |

# Serializador para el registro de álbumes
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

# Serializador para el registro de archivos (imágenes, vídeos)
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'