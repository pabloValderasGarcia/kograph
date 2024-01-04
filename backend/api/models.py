from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from backend.managers import CustomUserManager

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

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title