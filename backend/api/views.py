# | ---------------------------------------------------------------------- |
# | ---------------------- IMPORTACIONES NECESARIAS ---------------------- |
# | ---------------------------------------------------------------------- |

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.tokens import default_token_generator    
from rest_framework.parsers import MultiPartParser, FormParser
from djoser.serializers import PasswordResetConfirmSerializer
from django.contrib.auth.decorators import login_required
from backend.serializers import PasswordResetSerializer
from templated_mail.mail import BaseEmailMessage
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import Throttled
from backend.serializers import FileSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404, FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from djoser.conf import settings
from decouple import config
from .models import File
from djoser import utils
import os

# Obtener información sobre los métodos HTTP
@api_view(['OPTIONS'])
@permission_classes([AllowAny])
def options_view():
    return Response()

# | --------------------------------------------------------------------------- |
# | ---------------------- AWS (INTELIGENCIA ARTIFICIAL) ---------------------- |
# | --------------------------------------------------------------------------- |

# AWS Credenciales
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')
aws_session_token = config('aws_session_token')
aws_region = config('aws_region')

# | ---------------------------------------------------------------- |
# | ---------------------- EMAIL Y CONTRASEÑA ---------------------- |
# | ---------------------------------------------------------------- |

# Vista para enviar enlace de activación de cuenta
class ActivationAccount(BaseEmailMessage):
    template_name = "email/activation_account.html"

    def get_context_data(self):
        context = super().get_context_data()

        # Obtención de parámetros necesarios para el mensaje del correo
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["domain"] = os.getenv("FRONTEND_BASE_URL").split('://', 1)[-1]
        context["site_name"] = os.getenv("APP_NAME")

        return context

# Vista para enviar enlace de reseteo de contraseña
class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()

        # Obtención de parámetros necesarios para el mensaje del correo
        user = context.get("user")
        user_id = user.pk

        # Verificar que el correo ya ha sido enviado para evitar ataques DDoS
        last_reset_email_time = cache.get(f'reset_email_sent_{user_id}')
        if last_reset_email_time:
            time_difference = timezone.now() - last_reset_email_time
            if time_difference.total_seconds() < 300:
                raise Throttled(detail='Please, wait approximately 5 minutes from your last request.')
        
        # Obtención de parámetros necesarios para el mensaje del correo
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["domain"] = os.getenv("FRONTEND_BASE_URL").split('://', 1)[-1]
        context["site_name"] = os.getenv("APP_NAME")

        # Guardamos en cache el tiempo que ha pasado desde que el correo fue enviado (para comparar arriba)
        cache.set(f'reset_email_sent_{user.pk}', timezone.now())
        
        return context
        
# Vista para verificar el reseteo de contraseña en frontend
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Usamos el serializador de contraseña
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Iniciamos las variables necesarias
        new_password = request.data.get('new_password')
        re_new_password = request.data.get('re_new_password')
        uid = kwargs.get('uid')
        
        # Verificamos si el usuario está autenticado
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = get_object_or_404(get_user_model(), pk=uid)

        # Verificamos si ambas contraseñas son iguales
        if new_password != re_new_password:
            return Response({'detail': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Guardamos contraseña y usuario
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)
    
# Vista para verificar que existe el usuario con x email registrado
class CheckEmail(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        # Iniciamos las variables necesarias y comprobamos si existe
        User = get_user_model()
        email = request.GET.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            return Response(True)
        else:
            return Response(False)
        
# Vista para verificar enlaces válidos
class ValidateLinkView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_generator = default_token_generator

    def get(self, request):
        # Iniciamos las variables necesarias
        uid = request.GET.get('uid')
        token = request.GET.get('token')

        # Verificamos si el token ha sido usado (a través de caché)
        activation_token_used = cache.get('activation_token_used')
        if activation_token_used:
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
        cache.set('activation_token_used', True)

        # A través de serializadores comprobamos que sea válido
        serializer = PasswordResetConfirmSerializer(
            data={'uid': uid, 'token': token, 'new_password': 'temp_password'},
            context={'request': request, 'view': self, 'token_generator': self.token_generator}
        )
        if serializer.is_valid():
            return Response({'detail': 'Reset link is valid.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
        
# | -------------------------------------------------------------------------------- |
# | ---------------------- MANEJO DE FICHEROS (imagen, vídeo) ---------------------- |
# | -------------------------------------------------------------------------------- |
        
# Vista para subir archivo
class UploadFile(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Iniciamos variables necesarias
        user_id = str(request.user.id)
        file_data = request.FILES.get('file')
        title = request.data.get('title')
        serializer = FileSerializer(data={'user': user_id, 'file': file_data, 'title': title})

        # Verificamos que sea válido
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Image uploaded successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Vista para conseguir imagen de forma privada (en producción)
@login_required
def serve_protected_file(request, file_path):
    print('a')
    user = request.user

    # File correspondiente al archivo solicitado
    file = get_object_or_404(File, file="files/" + file_path)

    # Verifica si el usuario tiene permisos para acceder al archivo
    if file.user != user:
        raise Http404("You don't have access to this file.")

    # Construye la ruta completa al archivo
    full_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

    # Sirve el archivo usando FileResponse
    response = FileResponse(open(full_path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={file_path}'

    return response
        
# Vista para conseguir todas las imágenes (ALL)
class AllImages(APIView):
    def get(self, request):
        # Iniciamos variables necesarias
        user_id = request.user.id
        user_images = File.objects.filter(user_id=user_id)
        serializer = FileSerializer(user_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)