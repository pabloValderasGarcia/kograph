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
from django.conf import settings
from django.db import models
import hashlib
import magic
import time
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
                regex=r'^[a-zA-Z0-9_\.\-]{1,20}',
                message="Username must contain letters, numbers, or special characters (_.)."
            ),
            MinLengthValidator(1, 'Username must be at least 1 character.'),
            MaxLengthValidator(20, 'Username cannot be more than 20 characters.'),
        ]
    )
    picture = models.CharField(max_length=255, blank=True)
    activation_token_used = models.BooleanField(default=False)

# Modelo álbum para manejar sus campos
class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

# Modelo archivo para manejar sus campos
class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='files', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='files/')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=50, default='image')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    aws_tags = models.CharField(max_length=1000, blank=True, null=True)
    aws_feelings = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    origin_created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.origin_created_at:
            # Asigna un valor predeterminado basado en la fecha actual
            self.origin_created_at = timezone.now()
        super().save(*args, **kwargs)
    
    # Función para verificar que el fichero sea imagen o vídeo (a través de su MIME)
    def clean(self):
        print(self.file)
        mime = magic.Magic()
        file_type = mime.from_buffer(self.file.read(1024))
        return 'image' in file_type or 'video' in file_type
        
    def delete(self, *args, **kwargs):
        # Eliminar el fichero principal
        if self.file:
            try:
                file_path = os.path.join(settings.BASE_DIR, 'files', os.path.basename(str(self.file)))
                os.remove(file_path)
            except FileNotFoundError:
                print(f"File '{file_path}' not found.")
            except Exception as e:
                print(f"Error trying to delete file '{file_path}': {e}")

        # Eliminar el thumbnail
        if self.thumbnail:
            try:
                thumbnail_path = os.path.join(settings.BASE_DIR, 'thumbnails', str(os.path.basename(str(self.thumbnail))) + '.png')
                os.remove(thumbnail_path)
            except FileNotFoundError:
                print(f"Thumbnail {thumbnail_path} not found.")
            except Exception as e:
                print(f"Error trying to delete thumbnail '{file_path}': {e}")

        super().delete(*args, **kwargs)

    # Función que comprueba si la imagen ya existe con los mismos bytes (o píxeles)
    def is_duplicate(self, new_file_data):
        # Calcular el hash del archivo existente
        with open(self.file.path, 'rb') as existing_file:
            existing_hash = hashlib.sha256(existing_file.read()).hexdigest()

        # Calcular el hash del nuevo archivo
        new_hash = hashlib.sha256(new_file_data).hexdigest()

        # Comparamos los hashes
        return existing_hash == new_hash