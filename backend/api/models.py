# | ---------------------------------------------------------------------- |
# | ---------------------- IMPORTACIONES NECESARIAS ---------------------- |
# | ---------------------------------------------------------------------- |

from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from backend.managers import CustomUserManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
import magic
import os

# | ------------------------------------------------------- |
# | ---------------------- FUNCIONES ---------------------- |
# | ------------------------------------------------------- |

def is_valid_file(value):
    # Iniciamos las variables necesarias
    mime = magic.Magic()
    file_mime_type = mime.from_buffer(value.read(1024))

    # Verificar si es un tipo MIME de imagen o video
    if not file_mime_type.startswith('image/') and not file_mime_type.startswith('video/'):
        raise ValidationError(_("Invalid file type. Only image and video files are allowed."))
    
# | ----------------------------------------------------- |
# | ---------------------- MODELOS ---------------------- |
# | ----------------------------------------------------- |

# Modelo usuario para manejar sus campos
class User(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9_\.\-]{1,20}',
                message="Username must contain letters, numbers, or special characters (_.)."
            ),
            MinLengthValidator(1, 'Username must be at least 1 character.'),
            MaxLengthValidator(20, 'Username cannot be more than 20 characters.'),
        ]
    )
    activation_token_used = models.BooleanField(default=False)

# Modelo archivo para manejar sus campos
class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def clean(self):
        mime = magic.Magic()
        file_type = mime.from_file(self.file.path)
        if 'image' not in file_type and 'video' not in file_type:
            raise ValidationError(_("Invalid file type. Only images and videos are allowed."))
        
    def delete(self, *args, **kwargs):
        if self.file_field:
            os.remove(self.file_field.path)

        super().delete(*args, **kwargs)